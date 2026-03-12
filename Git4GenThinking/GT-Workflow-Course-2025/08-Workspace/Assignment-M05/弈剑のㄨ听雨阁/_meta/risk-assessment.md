---
type: protocol
---

# 🚦 智能体操作风险分级表

## 🔴 高风险 (High Risk) - 必须人工确认
> 此类操作可能导致数据永久丢失，Agent 禁止自动执行。

| 操作类型 | 描述 | 恢复手段 |
| :--- | :--- | :--- |
| **Delete** | 删除笔记或文件 | 仅回收站/Git |
| **Overwrite** | 覆盖现有文件内容 | Git 回滚 |
| **Bulk Rename** | 批量重命名 > 5 个文件 | 极其繁琐 |

## 🟡 中风险 (Medium Risk) - 需事后通知
> Agent 可执行，但必须在 Daily Note 中生成报告。

| 操作类型 | 描述 |
| :--- | :--- |
| **Merge** | 合并两个概念的内容 |
| **Move** | 移动文件目录 |
| **Modify Metadata** | 修改 YAML 状态 (如 draft -> review) |

## 🟢 低风险 (Low Risk) - 全自动
> 允许 Agent 后台静默执行。

| 操作类型 | 描述 |
| :--- | :--- |
| **Read** | 读取文件内容 |
| **Create** | 创建新文件 |
| **Tag** | 添加标签 |
| **Log** | 写入日志 |
