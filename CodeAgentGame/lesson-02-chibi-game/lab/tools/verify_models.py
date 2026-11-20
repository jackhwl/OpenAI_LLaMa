import json, urllib.request, urllib.error, base64, os

# 令牌不写死在源码里：优先读 ../config.json，其次读环境变量 MOARK_KEY
def _load_key():
    import json as _j, os as _o, pathlib as _p
    for _c in (_p.Path(__file__).resolve().parent.parent / "config.json",
               _p.Path(__file__).resolve().parent.parent / "config.example.json"):
        if _c.exists():
            try:
                _k = _j.loads(_c.read_text(encoding="utf-8")).get("api_key", "")
                if _k and not _k.startswith("<<"):
                    return _k
            except Exception:
                pass
    return _o.environ.get("MOARK_KEY", "")

K = _load_key()
if not K:
    raise SystemExit("未找到令牌：请复制 ../config.example.json 为 ../config.json 并填入 api_key")
BASE = "https://api.moark.com/v1"
OUT = "chibi-game/assets"
os.makedirs(OUT, exist_ok=True)

SCENE = ("【场景】208年冬，赤壁。曹操二十万大军沿长江北岸扎营，战船首尾相连。"
         "周瑜的火攻计划需要东南风，但此刻江上刮的是西北风。"
         "【抉择】A 继续等风  B 强行出击  C 先烧北岸旱寨制造混乱")
SYS = "你是《三国演义》风格的战史叙述者。文风凝练、有画面感，不溢美、不虚构具体数字，控制在120字内。"

print("======== 多模型参谋团对比 ========")
COUNCIL = ["GLM-5.3", "Qwen3.6-27B", "Qwen3.6-35B-A3B", "InternVL3-78B",
           "internlm3-8b-instruct", "Fin-R1", "Intern-S2", "HY-MT2-7B"]

for m in COUNCIL:
    body = json.dumps({"model": m, "messages": [
        {"role": "system", "content": SYS},
        {"role": "user", "content": SCENE + "\n\n只输出你的判断与理由，90字内。"}],
        "max_tokens": 400, "temperature": 0.8}).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + K,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            d = json.loads(r.read().decode())
            c = (d["choices"][0]["message"].get("content") or "").strip()
            u = d.get("usage", {})
            print(f"\n--- {m}  (tokens={u.get('total_tokens')}) ---\n{c[:300] if c else '[空响应]'}")
    except urllib.error.HTTPError as e:
        print(f"\n--- {m} --- HTTP {e.code}: {e.read().decode()[:120]}")
    except Exception as e:
        print(f"\n--- {m} --- ERR {e}")

print("\n\n======== IndexTTS-2 语音落盘 ========")
REF = "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav"
body = json.dumps({"model": "IndexTTS-2",
                   "input": "东风不与周郎便，铜雀春深锁二乔。",
                   "prompt_audio_url": REF}).encode()
req = urllib.request.Request(BASE + "/audio/speech", data=body,
                             headers={"Authorization": "Bearer " + K,
                                      "Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=180) as r:
    raw = r.read()
    print("ctype:", r.headers.get("Content-Type"), "bytes:", len(raw))
p = os.path.join(OUT, "tts-sample.wav")
open(p, "wb").write(raw)
print("saved:", p, os.path.getsize(p))
