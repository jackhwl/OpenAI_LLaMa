# -*- coding: utf-8 -*-
"""叙事模型延迟 / 质量基准测试。"""
import json, time, urllib.request, urllib.error

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

SYS = ("你是《三国演义》风格的战史叙述者。文风凝练、有画面感。"
       "只用汉末三国的词汇，不出现现代术语，不虚构精确数字。")
USER = ("【节点】建安十三年十一月 连船\n【所选】火攻，烧其连船\n"
        "【态势】水战 5→8，天时 5→6，曹疑 5→6\n\n"
        "写这个决策带来的直接后果，只写这一幕，100-150字，直接输出正文。")

MODELS = ["GLM-5.3", "InternVL3-78B", "internlm3-8b-instruct", "HY-MT2-7B",
          "Fin-R1", "Qwen3.6-27B", "Qwen3.6-35B-A3B", "Lingshu-32B",
          "Qwen3-Coder-30B-A3B-Instruct", "Atria-Dawn-Free"]

rows = []
for m in MODELS:
    body = json.dumps({"model": m,
                       "messages": [{"role": "system", "content": SYS},
                                    {"role": "user", "content": USER}],
                       "max_tokens": 8000, "temperature": 0.9}).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + K,
                                          "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.loads(r.read().decode())
        dt = time.time() - t0
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        rt = (msg.get("reasoning_content") or "")
        rows.append((m, dt, len(txt), len(rt), txt))
        print(f"{m:26} {dt:6.1f}s  正文{len(txt):4}字  思维链{len(rt):5}字")
    except Exception as e:
        print(f"{m:26} {time.time()-t0:6.1f}s  失败: {str(e)[:50]}")

print("\n" + "=" * 78)
print("按速度排序（正文非空者）")
for m, dt, n, rt, txt in sorted([r for r in rows if r[2] > 0], key=lambda x: x[1]):
    print(f"\n--- {m}  [{dt:.1f}s] ---\n{txt[:180]}")
