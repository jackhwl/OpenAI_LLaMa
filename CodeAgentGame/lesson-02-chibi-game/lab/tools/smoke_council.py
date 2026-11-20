# -*- coding: utf-8 -*-
import json, urllib.request

req = urllib.request.Request(
    "http://127.0.0.1:8848/api/council",
    data=json.dumps({
        "sceneTitle": "建安十三年七月 江陵的军械",
        "sceneText": "刘表病亡，其子刘琮已遣使向曹操请降。江陵城中囤有军械战船，此刻无主。轻骑急趋十日可至。",
        "options": [
            {"key": "A", "label": "轻骑急趋江陵", "detail": "抢在曹军之前尽取军械"},
            {"key": "B", "label": "退保夏口", "detail": "与刘琦合兵稳守"},
            {"key": "C", "label": "焚毁江陵积储", "detail": "不留与曹操"},
        ],
    }, ensure_ascii=False).encode("utf-8"),
    headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=300) as r:
    d = json.loads(r.read().decode("utf-8"))
if d.get("error"):
    print("ERROR:", d["error"])
for o in d.get("opinions", []):
    print(f"  {o['title']:14} {o['model']:24} {o['text'][:76]}")
