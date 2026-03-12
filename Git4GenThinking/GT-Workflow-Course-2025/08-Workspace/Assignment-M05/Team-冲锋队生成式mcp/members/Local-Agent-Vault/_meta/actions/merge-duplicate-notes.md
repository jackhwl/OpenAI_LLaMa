---
action_type: MERGE_NOTES
risk_level: MEDIUM
---
## 目标
减少 GraphRAG 中的重复节点
## 触发条件
- 相似度 > 高
- 多个概念指向同一结论
## Dry-run 方案
列出建议合并的笔记对，不直接修改
## 成功标准
- 合并后孤立节点减少
