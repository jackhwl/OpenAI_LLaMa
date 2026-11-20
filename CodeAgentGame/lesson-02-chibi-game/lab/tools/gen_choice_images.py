# -*- coding: utf-8 -*-
"""
《赤壁·风起》—— 为 15 个抉择各生成一张横幅插画。

特点：
  - 断点续跑：已生成的选项直接跳过，不重复消耗额度
  - 模型降级链：Qwen-Image-2512 -> FLUX.1-dev -> Kolors -> z-image-turbo
  - 生成后自动压成 JPEG（1120px / q82），否则 15 张 PNG 约 20MB
  - 产物写入 assets/choices/，并生成 manifest.json 供前端读取图片路径与提示词

用法：
  python tools/gen_choice_images.py              # 生成全部缺失的
  python tools/gen_choice_images.py --only 3A,4B # 只补指定的
"""
import base64
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # chibi-game/
OUT = os.path.join(ROOT, "assets", "choices")
TMP = os.path.join(OUT, "_raw")
os.makedirs(TMP, exist_ok=True)

CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
KEY = CFG["api_key"]
BASE = "https://api.moark.com/v1"
SIZE = CFG.get("image_size", "1024x768")
MODELS = [CFG.get("image_model", "Qwen-Image-2512")] + list(CFG.get("image_fallback", []))

MAGICK = shutil.which("magick") or r"S:\openclaw-tools\portable\imagemagick\magick.exe"

# 统一的画风约束 —— 与被讲解的"约束性提示词"是同一套思路
STYLE = ("中国汉末三国题材，水墨与工笔重彩相融，宣纸肌理，赭石与青绿为主调，"
         "光影厚重，气势恢宏，横构图；画面中不出现任何文字、印章、题跋或水印")

JOBS = [
    # 一 · 江陵的军械
    ("1A", "轻装骑兵沿驿道疾驰，尘埃飞扬，远处汉代城郭与长江水色，暮色苍茫"),
    ("1B", "汉末江夏水口，战船列阵于江岸水寨，守军布防，江面烟波浩渺"),
    ("1C", "汉末粮仓与军械库腾起大火，浓烟冲天，士卒四散撤离，火光映红天际"),
    # 二 · 案上那一剑
    ("2A", "汉末军帐内烛火摇曳，二人对坐结盟，案上铺开盟书与一柄长剑，气氛庄重"),
    ("2B", "使者持书卷步出军帐，帐内暗处兵甲林立，隐约的密谋气息"),
    ("2C", "江边渡口，使者持节杖与展开的地图，江东船只待发，天色阴沉"),
    # 三 · 连船
    # 注意：第一版写成"铁索相连的战船"，模型画成了「铁索桥」。必须写清"船与船彼此锁连"并排除桥梁
    ("3A", "数十艘汉末战船首尾相接，用粗铁链互相锁连成一整排，其中数艘燃起熊熊大火，"
           "夜色长江，浓烟冲天，火光映红江面；画面中不出现任何桥梁"),
    ("3B", "月夜江面，水下潜行者手持短刃逼近敌船船底，暗流翻涌，气泡浮动"),
    ("3C", "汉末军队沿山间小径夜行，火把连成一线，江对岸敌营灯火连绵"),
    # 四 · 风向
    ("4A", "冬夜江边，一人独立仰望云气，江面平静如镜，远岸营火点点"),
    ("4B", "夜色中战船齐发，桨叶激起水花，火把照亮江面，杀气腾腾"),
    ("4C", "北岸旱寨燃起大火，烟柱直冲夜空，营中一片混乱奔走"),
    # 五 · 黄盖的降书
    ("5A", "十艘蒙冲斗舰顺风疾驰，船头堆满薪草膏油，火舌初起，江面起浪"),
    ("5B", "曹军水寨内部起火，士卒在浓烟中奔逃，内外火光相互呼应"),
    ("5C", "东吴轻舟直冲曹军水寨，箭雨纷飞，浪花拍击船头"),
]

LOCK = threading.Lock()


def say(msg):
    with LOCK:
        print(msg, flush=True)


def gen_one(prompt, timeout=300):
    """按降级链依次尝试，返回 (字节, 模型名, 耗时秒)。"""
    last = "未知错误"
    for model in MODELS:
        for attempt in (1, 2):
            body = json.dumps({"model": model, "prompt": prompt,
                               "n": 1, "size": SIZE}).encode("utf-8")
            req = urllib.request.Request(
                BASE + "/images/generations", data=body,
                headers={"Authorization": "Bearer " + KEY,
                         "Content-Type": "application/json"})
            try:
                t0 = time.time()
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    d = json.loads(r.read().decode("utf-8"))
                item = d["data"][0]
                b64 = item.get("b64_json")
                if b64:
                    return base64.b64decode(b64), model, time.time() - t0
                url = item.get("url")
                if url:
                    with urllib.request.urlopen(url, timeout=timeout) as r2:
                        return r2.read(), model, time.time() - t0
                last = "响应中既无 b64_json 也无 url"
            except urllib.error.HTTPError as e:
                detail = e.read()[:140].decode("utf-8", "ignore")
                last = f"{model} HTTP {e.code} {detail}"
            except Exception as e:
                last = f"{model} {type(e).__name__}: {str(e)[:110]}"
            say(f"      ! {last}")
            time.sleep(2)
    raise RuntimeError(last)


def work(idx, key, prompt):
    jpg = os.path.join(OUT, key + ".jpg")
    full = prompt + "。" + STYLE
    if os.path.exists(jpg):
        say(f"[{idx:2}/15] {key}  已存在，跳过")
        return key, "skip", full, ""
    say(f"[{idx:2}/15] {key}  生成中…  {prompt[:24]}")
    try:
        data, model, dt = gen_one(full)
        png = os.path.join(TMP, key + ".png")
        with open(png, "wb") as f:
            f.write(data)
        subprocess.run([MAGICK, png, "-resize", "1120x",
                        "-quality", "82", "-strip", jpg], check=True)
        os.remove(png)
        kb = os.path.getsize(jpg) // 1024
        say(f"          ✓ {key}  {model}  {dt:.0f}s  {kb}KB")
        return key, "ok", full, model
    except Exception as e:
        say(f"          ✗ {key}  失败：{str(e)[:150]}")
        return key, "fail", full, ""


def main():
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))

    todo = [(i, k, p) for i, (k, p) in enumerate(JOBS, 1) if not only or k in only]
    say(f"输出目录 : {OUT}")
    say(f"模型降级 : {' -> '.join(MODELS)}")
    say(f"画幅     : {SIZE}  →  输出 1120px JPEG")
    say(f"待生成   : {len(todo)} 张\n")

    results = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        for key, status, full, model in pool.map(lambda a: work(*a), todo):
            results[key] = (status, full, model)

    # 结尾统一按磁盘实际产物重建 manifest（中途被打断也不影响）
    manifest = {}
    for idx, (key, prompt) in enumerate(JOBS, 1):
        jpg = os.path.join(OUT, key + ".jpg")
        if os.path.exists(jpg):
            manifest[key] = {
                "img": f"assets/choices/{key}.jpg",
                "prompt": prompt + "。" + STYLE,
                "scene": (idx + 2) // 3,
                "kb": os.path.getsize(jpg) // 1024,
            }
    mpath = os.path.join(OUT, "manifest.json")
    json.dump(manifest, open(mpath, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    ok = sum(1 for s, _, _ in results.values() if s == "ok")
    skip = sum(1 for s, _, _ in results.values() if s == "skip")
    fail = sum(1 for s, _, _ in results.values() if s == "fail")
    say(f"\n本次：成功 {ok} / 跳过 {skip} / 失败 {fail}")
    say(f"磁盘现存图片 {len(manifest)} / 15，manifest 已写入 manifest.json")
    if len(manifest) < 15:
        say("提示：重跑本脚本会只补缺失的那几张。")


if __name__ == "__main__":
    main()
