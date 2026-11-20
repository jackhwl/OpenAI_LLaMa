import json, urllib.request, urllib.error, time

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

CANDIDATES = [
    # 决策 / 小模型
    "Intern-Decision-4B","NeoHorse-Jev-4B","SemIf-OpenJev-4B",
    "APUS-OpenJev-v1-9B","APUS-OpenJev-v1-4B","Bespoke-Nimble-9B",
    "Intern-S2","VajraV1","nonescape-v0",
    # 主力对话
    "deepseek-v4.1-flash","DeepSeek-V4-Pro","DeepSeek-V4-Flash",
    "qwen3.8-max","qwen3.8-max-0902","qwen3.8-flash","qwen3.8-27b",
    "GLM-5.3","GLM-5.3-Flash","GLM-5.2","GLM-5.1","GLM-5",
    "kimi-k3","Kimi-K2.6","MiniMax-H3","MiniMax-M3","MiniMax-M2.7",
    "Qwen3.5-Plus","Qwen3.7-Plus","Qwen3.7-Max","Qwen3.6-Plus","Qwen3.5-Flash",
    "Qwen3.8-Omni-Flash","Step-3.7-Flash","MiMo-V2.5-Pro","happyhorse-1.1",
    "laya-multilingual","HappyHorse-1.0","ERNIE-5.0-Thinking","qwen-max",
]

def probe_chat(model):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 3,
    }).encode()
    req = urllib.request.Request(
        BASE + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + K, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            d = json.loads(r.read().decode())
            return "OK", str(d.get("choices", [{}])[0].get("message", {}).get("content", ""))[:40]
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode()).get("error", {}).get("message", "")
        except Exception:
            msg = str(e)
        return "FAIL", msg[:70]
    except Exception as e:
        return "ERR", str(e)[:70]

ok, bad = [], []
for m in CANDIDATES:
    st, info = probe_chat(m)
    print(f"{st:5} | {m:26} | {info}", flush=True)
    (ok if st == "OK" else bad).append(m)
    time.sleep(0.25)

print("\n===== 可用 =====")
print("\n".join(ok) if ok else "(无)")
