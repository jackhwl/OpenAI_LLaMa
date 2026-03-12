# 第五章实验：在 Obsidian 中构建本地智能知识助手（RAG + GraphRAG + 行动链）

## 1. 实验目标
使用 Obsidian 作为本地知识工作台，构建一个具备 **检索 → 评估 → 行动 → 反思** 能力的智能知识助手原型（人工在回路）。

本 Vault 的示例主题选用：**“深度精读一篇 Object Navigation 论文”的最小可行工作流（MVW）**  
（原因：输入清晰、结构稳定、能自然产生概念卡与行动链。）

---

## 2. Vault 结构（可治理知识结构）
已采用统一目录结构（Memory/Goals/Reflect/Evaluate 物理载体）：

- `/notes`：论文原文摘要、精读笔记、问题列表（Memory）
- `/concepts`：概念卡（GraphRAG 节点）
- `/projects`：长期目标与周期任务（Goals）
- `/daily`：反思日志（Reflect）
- `/_meta`：规则、schema、行动链文档（Evaluate 的结构依据）
- `/_attachments`：截图与附件
- `/_templates`：模板

---

## 3. 元数据与分块策略（Chunking）
### 3.1 最小元数据标准（Properties）
每个笔记至少包含：
- `type: note | concept | project | source`
- `status: draft | active | review | stable`
- `tags: []`
- `created: YYYY-MM-DD`
- `updated: YYYY-MM-DD`

### 3.2 分块策略（人工 + 半自动）
- **规则：一个二级标题（##）= 一个 Chunk**
- 通过 Obsidian 全局搜索验证：
  - 一条搜索结果尽量对应一个完整观点
  - 混多个主题 → Chunk 太大；一个观点被拆散 → Chunk 太小

---

## 4. GraphRAG 实现方式（节点 + 边 + 社区）
### 4.1 节点（Concept Nodes）
在 `/concepts` 下维护概念卡，例如：
- `Chunking.md`
- `GraphRAG.md`
- `Action-Chain.md`
- `Object-Navigation.md`
- `Semantic-Map.md`
- `RL-vs-SLAM.md`

### 4.2 边（关系表达）
通过 Obsidian 原生双链在正文中形成“可遍历语义网络”，例如：
`[[Chunking]] supports [[GraphRAG]]`
`[[GraphRAG]] extends [[RAG]]`
`[[Object Navigation]] relates_to [[Semantic Map]]`

### 4.3 社区（人工版社区检测）
Graph View 里按 `tag: knowledge-engineering` 过滤观察聚类，并为聚类建立社区摘要卡：
- `/concepts/Community-Knowledge-Engineering.md`

---

## 5. Agentic Workflow（最小主动工作流）
本原型工作流（人在回路）：

1) **Retrieve**：搜索/回链定位候选笔记与概念  
2) **Evaluate**：依据 `/_meta` 的行动计划触发条件输出 dry-run 清单  
3) **Act**：人工执行合并/补链/加标签/整理结构  
4) **Reflect**：在 `/daily` 记录执行回顾与改进点，反哺下一轮 Evaluate

