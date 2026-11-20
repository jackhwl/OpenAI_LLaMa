# -*- coding: utf-8 -*-
"""
赤壁·风起  ——  本地 AI 代理服务

职责：
  1. 托管静态游戏页面
  2. 代理模力方舟（moark.com）的四类 AI 调用，API Key 只留在本机，不进浏览器

启动：  python server.py            （默认 http://127.0.0.1:8848）
依赖：  Python 标准库，无第三方包
"""

import base64
import hashlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, "assets", "cache")
CONFIG = os.path.join(ROOT, "config.json")

BASE = "https://api.moark.com/v1"
# 语音克隆用的参考音频（必须是公网可达的音频地址）
REF_AUDIO = "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav"

os.makedirs(CACHE, exist_ok=True)


# ---------------------------------------------------------------- 配置
def load_config():
    key = os.environ.get("MOARK_API_KEY", "").strip()
    cfg = {}
    if os.path.exists(CONFIG):
        try:
            cfg = json.load(open(CONFIG, encoding="utf-8"))
            key = key or cfg.get("api_key", "").strip()
        except Exception as e:
            print("  [config] 读取失败:", e)
    if not key:
        print("\n  !! 没有找到 API Key。")
        print("     请在 config.json 里填 api_key，或设置环境变量 MOARK_API_KEY\n")
    return key, cfg


API_KEY, CFG = load_config()

# 各角色的模型分工（全部经过实测，均为本资源包可用）
COUNCIL = CFG.get("council", [
    {"model": "GLM-5.3",               "persona": "主谋",   "title": "都督府 · 主谋",   "max_tokens": 2600},
    {"model": "InternVL3-78B",         "persona": "老将",   "title": "军中 · 老将",     "max_tokens": 500},
    {"model": "Fin-R1",                "persona": "算者",   "title": "度支 · 算者",     "max_tokens": 500},
    {"model": "HY-MT2-7B",             "persona": "水客",   "title": "江上 · 水客",     "max_tokens": 500},
    {"model": "internlm3-8b-instruct", "persona": "书佐",   "title": "幕府 · 书佐",     "max_tokens": 500},
])
NARRATOR = CFG.get("narrator", "internlm3-8b-instruct")
# 三种笔法。推理型模型思维链长、耗时数十秒，故只作为"史笔"备选，默认走快笔。
# 2026-11-12 复核：工笔原配 Qwen3-VL-30B-A3B-Instruct 已被平台停用（400），
# 换成课程实测过的 Qwen3-Coder-30B（同参数 2.3s，叙述画面感足够）。
NARRATOR_STYLES = CFG.get("narrator_styles", {
    "fast":    {"label": "快笔", "model": "internlm3-8b-instruct", "max_tokens": 1200},
    "sharp":   {"label": "工笔", "model": "Qwen3-Coder-30B-A3B-Instruct", "max_tokens": 1600},
    "classic": {"label": "史笔", "model": "GLM-5.3", "max_tokens": 8000},
})
# 任一笔法失败时的兜底顺序（实测：这几个不出正文以外的错，响应也快）
NARRATOR_FALLBACK = CFG.get("narrator_fallback", [
    {"model": "internlm3-8b-instruct", "max_tokens": 1200},
    {"model": "InternVL3-78B", "max_tokens": 1600},
])
IMAGE_MODEL = CFG.get("image_model", "Qwen-Image-2512")
IMAGE_FALLBACK = CFG.get("image_fallback", ["FLUX.1-dev", "Kolors", "z-image-turbo"])
# 注意：该平台只接受固定画幅，实测 1024x1024 / 1024x768 有效，1152x864、1280x720 会被拒
IMAGE_SIZE = CFG.get("image_size", "1024x768")
TTS_MODEL = CFG.get("tts_model", "IndexTTS-2")


# ---------------------------------------------------------------- 底层调用
def _post(path, payload, timeout=180):
    # 无令牌时不要在这里静默发出空令牌请求 —— 给一句人话。
    # 注意：命中 assets/cache 的图片与配音根本走不到这里，所以没令牌也能复用它们。
    if not API_KEY:
        raise RuntimeError("未配置 API Key，请检查 config.json")
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + API_KEY,
                 "Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def call_chat(model, messages, max_tokens=600, temperature=0.85, timeout=180):
    """返回纯文本。推理型模型的思维链会先被消耗 token，故 max_tokens 给得较宽。"""
    raw = _post("/chat/completions", {
        "model": model, "messages": messages,
        "max_tokens": max_tokens, "temperature": temperature,
    }, timeout=timeout)
    d = json.loads(raw.decode("utf-8"))
    msg = d["choices"][0]["message"]
    return (msg.get("content") or "").strip()


def call_image(model, prompt, size=None, timeout=300):
    raw = _post("/images/generations",
                {"model": model, "prompt": prompt, "n": 1,
                 "size": size or IMAGE_SIZE},
                timeout=timeout)
    d = json.loads(raw.decode("utf-8"))
    item = d["data"][0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as r:
            return r.read()
    raise RuntimeError("生图返回里没有图像数据")


def call_tts(text, timeout=300):
    raw = _post("/audio/speech",
                {"model": TTS_MODEL, "input": text, "prompt_audio_url": REF_AUDIO},
                timeout=timeout)
    if raw[:4] == b"RIFF" or raw[:3] == b"ID3" or raw[:2] == b"\xff\xfb":
        return raw
    raise RuntimeError("语音返回不是音频: " + raw[:120].decode("utf-8", "ignore"))


def cache_path(tag, ext):
    p = os.path.join(CACHE, tag + ext)
    if os.path.exists(p) and os.path.getsize(p) > 256:
        return p, True
    return p, False


def digest(*parts):
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------- 提示词
# 提示词**只**存在于同目录 prompts/ 下的文件里。想换题材（比如把赤壁改成你家乡的战役），
# 改 prompts/ 里的文件即可，不必动本文件。
#
# 这里刻意**不再留内置副本**。早先的版本把同一份提示词抄在 server.py 里，文件读不到时
# 静默回落 —— 后果是学员改了 prompts/*.txt 却毫无效果（2026-10-27 学员试做挖出来的），
# 而且那份副本里写死了"汉末三国""曹操孙权"，换题材时它才是真正漏改的那一处。
# 现在缺文件直接报错，并把恢复命令写在错误信息里。
PROMPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")

REQUIRED_PROMPTS = [
    "narrator_system.txt", "base_rules.txt", "consequence_user.txt",
    "ending_system.txt", "ending_user.txt",
    "council_system.txt", "council_user.txt",
    "image_style.txt", "stat_labels.json",
]


def missing_prompts():
    return [n for n in REQUIRED_PROMPTS
            if not os.path.isfile(os.path.join(PROMPT_DIR, n))]


def load_prompt(name):
    """读 prompts/<name>。以 ## 开头的行是给学员看的注释，不发给模型。

    用 splitlines(keepends=True) 而不是 read().splitlines()：后者会吃掉文件末尾的
    换行，而那一个换行是真的会发给模型的（它分隔 prompt 与下一个段落）。
    """
    p = os.path.join(PROMPT_DIR, name)
    try:
        with open(p, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        raise RuntimeError(
            f"缺少提示词文件 prompts/{name}。"
            f"提示词不在代码里，丢了请在仓库根目录下执行 "
            f"`python tools/gen_prompts.py` 重新生成。")
    return "".join(l for l in text.splitlines(keepends=True)
                   if not l.startswith("##"))


def render(name, **kw):
    """读模板并按 {占位符} 替换。

    用 replace 而不是 str.format：模板里有货真价实的 JSON 花括号，format 会炸。
    """
    t = load_prompt(name)
    for k, v in kw.items():
        t = t.replace("{" + k + "}", str(v))
    return t


def load_stat_labels():
    """四个态势维度的显示名与补注。换题材改 prompts/stat_labels.json。

    同样不留内置副本：多一个逗号、少一层引号都会在这里当场报错，
    比静默退回赤壁的默认值要好。
    """
    p = os.path.join(PROMPT_DIR, "stat_labels.json")
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except OSError:
        raise RuntimeError(
            "缺少提示词文件 prompts/stat_labels.json。"
            "丢了请在仓库根目录下执行 `python tools/gen_prompts.py` 重新生成。")
    except ValueError as e:
        raise RuntimeError(f"prompts/stat_labels.json 不是合法 JSON：{e}")
    return d.get("labels") or {}, d.get("notes") or {}


def prompt_consequence(scene_title, choice_label, choice_detail, stats_before, stats_after):
    sysmsg = render("narrator_system.txt", base_rules=load_prompt("base_rules.txt"))
    labels, notes = load_stat_labels()
    parts = []
    for k in ("morale", "naval", "fortune", "cao"):
        parts.append(f"{labels.get(k, k)} {stats_before.get(k, '?')}→{stats_after.get(k, '?')}"
                     + notes.get(k, ""))
    delta = "，".join(parts) + "。"
    user = render(
        "consequence_user.txt",
        scene_title=scene_title, choice_label=choice_label,
        choice_detail=choice_detail, delta=delta,
    )
    return sysmsg, user


def prompt_ending(ending_title, history_lines, stats):
    sysmsg = render("ending_system.txt", base_rules=load_prompt("base_rules.txt"))
    labels, _ = load_stat_labels()
    final = "，".join(f"{labels.get(k, k)} {stats.get(k, '?')}"
                     for k in ("morale", "naval", "fortune", "cao"))
    user = render(
        "ending_user.txt",
        ending_title=ending_title, history="\n".join(history_lines), final=final,
    )
    return sysmsg, user


def prompt_council(scene_title, scene_text, options):
    sysmsg = load_prompt("council_system.txt")
    opts = "\n".join(f"{o['key']}. {o['label']}——{o['detail']}" for o in options)
    user = render(
        "council_user.txt",
        scene_title=scene_title, scene_text=scene_text, options=opts)
    return sysmsg, user


# ---------------------------------------------------------------- 业务
_STATUS_LOCK = threading.Lock()


def _council_prompt(body):
    return prompt_council(body["sceneTitle"], body["sceneText"], body["options"])


def ask_member(c, sysmsg, user):
    """问一位谋士。任何一位失手都不影响其余几位。

    带一个 ok 标记：没配上 Key、模型超时这类失败要在页面上让人一眼看见，
    而不是裹在一句体面的台词里，让人以为是模型"说了句场面话"。

    429 会退避重试一次：五个模型同时发出去，平台的 RPM 限流很容易被撞上
    （实测五个里最慢的那位撞过一次）。撞上不算这位谋士不会说话，隔两秒再问就好。
    """
    fail = lambda why: {"model": c["model"], "persona": c["persona"],
                        "title": c["title"], "text": why, "ok": False}
    for attempt in (1, 2):
        try:
            txt = call_chat(c["model"],
                            [{"role": "system", "content": sysmsg},
                             {"role": "user", "content": user}],
                            max_tokens=c.get("max_tokens", 500), timeout=200)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                time.sleep(2.5)
                continue
            hint = "（平台限流，隔几秒点「重试」）" if e.code == 429 else ""
            return fail(f"未能应答：上游 {e.code} {hint}".strip())
        except Exception as e:
            return fail(f"未能应答：{str(e)[:60]}")
        if not txt:
            return fail("未能应答：模型返回空正文（推理型模型常把额度烧在思维链上）")
        return {"model": c["model"], "persona": c["persona"],
                "title": c["title"], "text": txt, "ok": True}
    return fail("未能应答：连续两次被限流")


def op_council(body):
    """一次问完全部谋士（批量接口，供脚本调用，见 lab/tools/smoke_council.py）。"""
    sysmsg, user = _council_prompt(body)
    with ThreadPoolExecutor(max_workers=len(COUNCIL)) as ex:
        return {"opinions": list(ex.map(lambda c: ask_member(c, sysmsg, user), COUNCIL))}


def op_council_one(body):
    """一次只问一位谋士 —— 页面用它做「谁先想完谁先开口」。

    五个快慢差得远（实测 0.9 秒到几十秒），批量接口会让人干等最慢的那位，
    屏幕上只有一句"正在思量"，看上去跟卡死一样。拆成单路之后，
    每回来一位就补一张卡片，等待是有形状的。
    """
    sysmsg, user = _council_prompt(body)
    i = int(body.get("index", 0))
    if not 0 <= i < len(COUNCIL):
        raise RuntimeError(f"没有第 {i} 位谋士（共 {len(COUNCIL)} 位）")
    return {"opinion": ask_member(COUNCIL[i], sysmsg, user),
            "index": i, "total": len(COUNCIL)}


def narrate(sysmsg, user, style="fast"):
    """先按所选笔法尝试，失败则走兜底链。空正文不算成功。"""
    chosen = NARRATOR_STYLES.get(style) or NARRATOR_STYLES["fast"]
    chain = [{"model": chosen["model"], "max_tokens": chosen.get("max_tokens", 1200)}]
    chain += [f for f in NARRATOR_FALLBACK if f["model"] != chosen["model"]]

    errs = []
    for n in chain:
        try:
            t = call_chat(n["model"],
                          [{"role": "system", "content": sysmsg},
                           {"role": "user", "content": user}],
                          max_tokens=n.get("max_tokens", 1500),
                          temperature=0.9, timeout=280)
            if t:
                return t, n["model"], chosen["label"]
            errs.append(f"{n['model']}: 正文为空")
        except Exception as e:
            errs.append(f"{n['model']}: {str(e)[:60]}")
    raise RuntimeError("叙事模型全部失败 → " + " | ".join(errs))


def op_narrate(body):
    if body.get("kind") == "ending":
        sysmsg, user = prompt_ending(body["title"], body["history"], body["stats"])
    else:
        sysmsg, user = prompt_consequence(
            body["sceneTitle"], body["choiceLabel"], body["choiceDetail"],
            body["before"], body["after"])
    text, used, label = narrate(sysmsg, user, body.get("style", "fast"))
    # 把 system 也一并返回：它才是人设与铁律所在。
    # 这门课的立场是「提示词全公开可查」——学员得看得见模型被下了什么约束，
    # 才谈得上判断它哪句话不可信。
    return {"text": text, "prompt": user, "system": sysmsg,
            "model": used, "styleLabel": label}


def load_image_style():
    """生图提示词的固定后缀。想换整套画风（比如写近代史），改 prompts/image_style.txt。"""
    return load_prompt("image_style.txt")


def op_image(body):
    prompt = body["prompt"] + load_image_style()
    tag = "img_" + digest(prompt)
    path, hit = cache_path(tag, ".png")
    if hit:
        return {"url": "/assets/cache/" + tag + ".png", "cached": True, "prompt": prompt}

    models = [IMAGE_MODEL] + list(IMAGE_FALLBACK)
    last = None
    for m in models:
        try:
            data = call_image(m, prompt)
            with open(path, "wb") as f:
                f.write(data)
            print(f"  [image] {m} -> {os.path.getsize(path)} bytes")
            return {"url": "/assets/cache/" + tag + ".png",
                    "cached": False, "model": m, "prompt": prompt}
        except Exception as e:
            last = f"{m}: {e}"
            print("  [image] 失败", last)
    raise RuntimeError("所有生图模型均失败：" + str(last))


def op_tts(body):
    text = body["text"]
    tag = "tts_" + digest(text)
    path, hit = cache_path(tag, ".wav")
    if hit:
        return {"url": "/assets/cache/" + tag + ".wav", "cached": True}
    data = call_tts(text)
    with open(path, "wb") as f:
        f.write(data)
    print(f"  [tts] {len(data)} bytes")
    return {"url": "/assets/cache/" + tag + ".wav", "cached": False}


def op_status(_body):
    chat = ([c["model"] for c in COUNCIL] +
            [s["model"] for s in NARRATOR_STYLES.values()])
    seen, uniq = set(), []
    for m in chat:
        if m not in seen:
            seen.add(m); uniq.append(m)
    return {
        "council": [c["model"] for c in COUNCIL],
        "narrator": {k: v["model"] for k, v in NARRATOR_STYLES.items()},
        "chat": uniq,
        "image": [IMAGE_MODEL] + list(IMAGE_FALLBACK),
        "tts": [TTS_MODEL],
        "key_loaded": bool(API_KEY),
    }


ROUTES = {
    "/api/council": op_council,
    "/api/council/one": op_council_one,
    "/api/narrate": op_narrate,
    "/api/image": op_image,
    "/api/tts": op_tts,
    "/api/status": op_status,
}

MIME = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
        ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp",
        ".wav": "audio/wav", ".mp3": "audio/mpeg", ".svg": "image/svg+xml"}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *a):
        if "/api/" in (self.path or ""):
            sys.stderr.write("  %s %s\n" % (self.command, self.path))

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        try:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            # 浏览器提前断开（刷新页面、关标签、关闭自动化脚本），
            # 此时服务端写响应必然失败。这不是错误，吞掉即可，
            # 否则控制台会刷出一长串吓人的 traceback。
            pass

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/":
            p = "/index.html"
        if p == "/api/status":
            return self._json(op_status({}))
        fp = os.path.normpath(os.path.join(ROOT, p.lstrip("/")))
        if not fp.startswith(ROOT) or not os.path.isfile(fp):
            return self._send(404, "not found", "text/plain; charset=utf-8")
        ext = os.path.splitext(fp)[1].lower()
        with open(fp, "rb") as f:
            self._send(200, f.read(), MIME.get(ext, "application/octet-stream"))

    def do_POST(self):
        p = self.path.split("?")[0]
        fn = ROUTES.get(p)
        if not fn:
            return self._json({"error": "未知接口 " + p}, 404)
        # 注意：这里**不要**统一拦「没有令牌就 500」。
        # 图片与配音会先查 assets/cache，命中就完全不需要令牌；结局判定更是纯本地算法。
        # 没有令牌时，只有真正要发请求的那一步才会报错（由 _post 抛出）。
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
        except Exception as e:
            return self._json({"error": "请求体解析失败: " + str(e)}, 400)
        try:
            self._json(fn(body))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:300]
            self._json({"error": f"上游 {e.code}: {detail}"}, 502)
        except Exception as e:
            self._json({"error": str(e)[:300]}, 500)


def main():
    port = int(os.environ.get("PORT", 8848))
    print("\n  赤壁 · 风起   —   本地 AI 代理")
    print("  " + "-" * 46)
    print(f"  API Key : {'已载入' if API_KEY else '缺失'}")
    print(f"  参谋团  : {', '.join(c['model'] for c in COUNCIL)}")
    print("  笔法    : " + " | ".join(f"{v['label']}={v['model']}"
                                      for v in NARRATOR_STYLES.values()))
    print(f"  生图    : {IMAGE_MODEL} ({IMAGE_SIZE}; fallback: {', '.join(IMAGE_FALLBACK)})")
    print(f"  语音    : {TTS_MODEL}")
    print("  " + "-" * 46)
    gone = missing_prompts()
    if gone:
        # 不在这里抛异常：先让页面起得来，学员看到的报错发生在真正要用到提示词的那一刀。
        print("  !! 缺少提示词文件：" + "、".join(gone))
        print("     仓库根目录下执行 python tools/gen_prompts.py 可重新生成")
        print("  " + "-" * 46)
    print(f"  打开    : http://127.0.0.1:{port}\n")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
