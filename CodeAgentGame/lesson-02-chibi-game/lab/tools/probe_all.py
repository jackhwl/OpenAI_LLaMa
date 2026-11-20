import json, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

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

ALL = [m["id"] for m in json.load(open("moark-models.json", encoding="utf-8"))["data"]]

IMAGE_HINT = ["image", "flux", "sd3", "stable-diffusion", "kolors", "cogview",
              "hidream", "qwen-image", "z-image", "longcat-image", "glm-image",
              "seedvr", "animesharp", "esrgan", "kontext", "wan2", "wan3"]
TTS_HINT = ["tts", "voxcpm", "cosyvoice", "chatt", "indextts", "spark-tts", "step-audio"]


def post(path, payload, timeout=45):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + K, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return "OK", r.read().decode()[:160]
    except urllib.error.HTTPError as e:
        try:
            return "FAIL", json.loads(e.read().decode()).get("error", {}).get("message", "")[:60]
        except Exception:
            return "FAIL", f"HTTP {e.code}"
    except Exception as e:
        return "ERR", str(e)[:60]


def chat(m):
    return m, post("/chat/completions",
                   {"model": m, "messages": [{"role": "user", "content": "hi"}], "max_tokens": 2})


def image(m):
    return m, post("/images/generations",
                   {"model": m, "prompt": "a red boat", "n": 1}, timeout=120)


def tts(m):
    return m, post("/audio/speech",
                   {"model": m, "input": "测试", "voice": "default"}, timeout=60)


def run(fn, models, label):
    print(f"\n########## {label} ##########")
    good = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        for m, (st, info) in ex.map(fn, models):
            if st == "OK":
                print(f"  OK   | {m:34} | {info[:90]}")
                good.append(m)
            elif "资源包" in info:
                print(f"  NOENT| {m:34}")
            elif "暂不支持" in info:
                print(f"  BADEP| {m:34}")
            else:
                print(f"  ???  | {m:34} | {info[:60]}")
    print(f"  --> 可用 {label}: {good}")
    return good


chatable = run(chat, ALL, "chat/completions 全量")
run(image, [m for m in ALL if any(h in m.lower() for h in IMAGE_HINT)], "images/generations")
run(tts, [m for m in ALL if any(h in m.lower() for h in TTS_HINT)], "audio/speech")
