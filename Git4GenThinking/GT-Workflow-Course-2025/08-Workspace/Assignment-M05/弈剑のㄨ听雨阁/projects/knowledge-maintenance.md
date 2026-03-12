---
type: project
status: active
---

# 🛠 知识库维护项目

## 🤖 自动化规则定义 (给 AI 看的逻辑)

### 规则 A：抓出“孤儿”笔记
**逻辑描述**:
如果一个概念笔记满足以下两个条件：
1. 没有被其他笔记链接 (入链数为 0)
2. 创建时间已经超过 7 天了 (说明被我遗忘了)
**执行动作**:
- 给它打上标签 `#需关注`
- 在仪表盘显示警告

### 规则 B：清理陈旧草稿
**逻辑描述**:
如果一个笔记满足：
1. 状态是 `status: draft` (草稿)
2. 上次修改时间是 30 天前
**执行动作**:
- 建议用户把它移到 `/_archive` (归档文件夹) 或者删除。


```dataview
LIST
FROM "concepts"
WHERE file.inlinks.length = 0
```

```dataview
TABLE updated as "最后更新"
FROM "concepts"
WHERE status = "draft"
SORT updated ASC
```
