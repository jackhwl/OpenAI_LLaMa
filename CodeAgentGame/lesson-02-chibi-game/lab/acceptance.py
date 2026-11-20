# -*- coding: utf-8 -*-
"""对本地代理做端到端验收。"""
import json, time, urllib.request

BASE = "http://127.0.0.1:8848"


def call(path, payload, timeout=420):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8")), time.time() - t0


print("=" * 66)
print("1) /api/status")
d, dt = call("/api/status", {})
print("   参谋团 :", d["council"])
print("   叙事链 :", d["narrator"])
print("   生图   :", d["image"])
print("   语音   :", d["tts"])
print("   key    :", d["key_loaded"], f"({dt:.1f}s)")

print("=" * 66)
print("2) /api/narrate  ——  决策后果")
d, dt = call("/api/narrate", {
    "kind": "consequence",
    "sceneTitle": "建安十三年十一月 连船",
    "choiceLabel": "火攻，烧其连船",
    "choiceDetail": "连船难散，一炬可破——但需风向",
    "before": {"morale": 5, "naval": 5, "fortune": 5, "cao": 5},
    "after":  {"morale": 5, "naval": 8, "fortune": 6, "cao": 6},
})
print("   模型:", d.get("model"), f"({dt:.1f}s)")
print("   正文:", (d.get("text") or d.get("error")))

print("=" * 66)
print("3) /api/narrate  ——  结局断语")
d, dt = call("/api/narrate", {
    "kind": "ending",
    "title": "东风有意 —— 赤壁大胜 · 三分天下",
    "history": ["第1决 建安十三年·七月：选A「轻骑急趋江陵」",
                "第2决 建安十三年·十月：选A「联刘抗曹」",
                "第3决 建安十三年·十一月：选A「火攻，烧其连船」",
                "第4决 决战前夜：选A「信他，等风」",
                "第5决 决战当夜：选A「黄盖诈降，蒙冲纵火」"],
    "stats": {"morale": 11, "naval": 14, "fortune": 9, "cao": 8},
})
print("   模型:", d.get("model"), f"({dt:.1f}s)")
print("   正文:", (d.get("text") or d.get("error")))

print("=" * 66)
print("4) /api/image")
d, dt = call("/api/image", {
    "prompt": "长江江面，吴军楼船与曹军水寨隔江对峙，铁索连舟，旌旗蔽江，冬季雾气，肃杀气象"})
print("   ", d.get("url") or d.get("error"), "| 模型:", d.get("model"), f"({dt:.1f}s)")

print("=" * 66)
print("5) /api/tts")
d, dt = call("/api/tts", {"text": "东风不与周郎便，铜雀春深锁二乔。"})
print("   ", d.get("url") or d.get("error"), f"({dt:.1f}s)")
print("=" * 66)
print("验收结束")
