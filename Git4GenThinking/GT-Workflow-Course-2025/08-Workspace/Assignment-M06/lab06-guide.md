# Lab06 — 本地优先智能体运行环境实验指南

> **实验主题：**  构建一个基于本地知识库、通过远程大模型推理、可持续运行的最小可行Agent（MVA）

---

## 1. 实验目标

完成本实验后，你将亲手构建一个：

- 以 **Obsidian** 作为本地知识与状态环境
- 通过**Cherry Studio**连接远程 LLM（Qwen / DeepSeek）
- 具备**Evaluate → Act → Reflect** 闭环
- 能够在真实知识工作中反复运行的 **Agentic Workflow 原型**


> 📌 本实验的目标不是“跑通某个 Agent 框架”，  而是让你第一次以系统设计者的视角，构建一个能持续为你工作的智能体环境。

---

## 2. 实验环境与工具准备

### 2.1 所需工具清单

|工具|角色定位|
|---|---|
|Obsidian|本地知识库（Memory / State / Act）|
|Cherry Studio|Agent 客户端（Evaluate / Planning / Reflection）|
|远程 LLM|推理能力（Qwen / DeepSeek）|

> ⚠️ 本实验不要求本地部署任何模型。

---

### 2.2 Cherry Studio 安装指南（简要）

1. 访问 Cherry Studio 官方发布页

2. 下载与你操作系统对应的版本（Windows / macOS / Linux）

3. 完成安装并启动


首次启动后，你将看到一个类似“多模型对话与 Agent 管理”的界面。

---

### 2.3 配置远程 LLM（Qwen / DeepSeek）

在 Cherry Studio 中完成以下配置：

1. 进入 **模型设置 / Provider 设置**

2. 选择你使用的远程模型提供方（如 Qwen / DeepSeek）

3. 填写：

    - API Key

4. 保存并测试连接


✅ 若能正常返回模型回复，即配置成功。

---

## 3. 实验一：构建本地知识运行环境（Obsidian）

### 3.1 创建实验专用 Vault

1. 打开 Obsidian

2. 新建一个 Vault，命名为：


```text
lab06-agent-runtime
```

---

### 3.2 建立最小知识结构（MVA）

在 Vault 中创建以下基础目录：

```text
vault/
├── notes/        # 原始知识笔记
├── concepts/     # 抽象概念节点
├── projects/     # 长期任务 / 目标
├── actions/      # 行动计划（Action Plan）
├── reflection/   # 反思记录
```

> 📌 不追求数量，只追求结构清晰。

---

### 3.3 创建示例知识内容

至少创建：

- 3 条 `notes`

- 2 条 `concepts`

- 1 条 `project`


并使用 Obsidian 的双向链接将它们连接起来。

---

## 4. 实验二：通过 Cherry Studio 进行 Evaluate（决策）

### 4.1 设计一个 Agent 任务

示例任务（可直接使用）：“请基于我当前的 Obsidian 知识结构，  帮我设计一个【每周知识整理】的行动计划。”

---

### 4.2 在 Cherry Studio 中执行 Evaluate

1. 打开 Cherry Studio

2. 使用远程 LLM

3. 明确要求模型输出 **结构化行动计划**


示例提示（简化版）：

```text
你是一个智能体规划器。
请为以下目标生成一个行动计划：
- 目标：每周整理 Obsidian 知识库
- 输出格式：步骤列表
- 区分 Evaluate 与 Act
```

---

### 4.3 保存行动计划

将模型输出的行动计划：

- 手动复制

- 保存为 Obsidian 中的一个文件，例如：


```text
actions/weekly-knowledge-review.md
```

---

## 5. 实验三：Act（人在回路的行动执行）

### 5.1 执行行动计划（人工确认）

根据 Action Plan：

- 创建新笔记

- 合并重复概念

- 补充链接或标签


⚠️ 本实验 **不允许自动修改文件**，必须由你手动执行。

---

### 5.2 标记执行状态

在行动计划中标记：

- `[x] 已完成`

- `[ ] 待执行`


体现 **Agent 在运行，而不是一次性生成**。

---

## 6. 实验四：Reflect（反思与系统改进）

### 6.1 生成反思问题

在 Cherry Studio 中输入：

```text
请反思刚才的行动过程：
- 哪些步骤是多余的？
- 哪些地方可以结构优化？
- 下次应如何调整行动计划？
```

---

### 6.2 写回 Obsidian

将反思结果写入：

```text
reflection/2025-xx-xx.md
```

反思内容至少包含：

- 一个问题

- 一个改进方向


---

## 7. 实验五：形成可运行的 Agentic Workflow

此时，你已经完成：

1. 本地知识环境（Obsidian）

2. 决策与规划（Cherry Studio + 远程 LLM）

3. 行动执行（人在回路）

4. 反思与记忆沉淀


请在 `README.md` 中，用 **一段话** 描述你的 Agentic Workflow：

- 触发条件

- 行动流程

- 反思机制


---

## 8. 实验提交要求

## 8.1 请提交以下内容：

1. **README.md**

    - 描述你的 Agentic Workflow

2. **Action Plan 文档**（至少 1 份）

3. **Reflection 文档**（至少 1 条）

4. **2 张截图**

    - Obsidian Graph View

    - Cherry Studio 工作界面

### 8.2 提交目录结构

```
<小组名字>/
├── README.md
├── action.md
├── reflection.md
└── screenshots/
    ├── graph-view.png
    └── workflow.png
```

### 8.2 README.md 模板（实验说明）

```markdown

# Lab06 — 本地智能体运行环境实验

## 1. 实验目标

本实验旨在构建一个最小可行智能体（MVA），
使其能够在本地知识环境中，借助远程 LLM 完成
“检索 → 决策 → 行动 → 反思”的持续工作流。

---

## 2. 运行环境说明

- 本地知识库：Obsidian
- 推理与规划：Cherry Studio
- 远程模型：
  - [ ] Qwen
  - [ ] DeepSeek
  - [ ] 其他（请注明）

---

## 3. 本地知识结构设计

简要说明你的 Obsidian 知识库结构，例如：

- 笔记类型（Notes / Concepts / Projects）
- 使用的标签或元数据字段
- 是否存在概念链接或主题聚合

---

## 4. Agentic Workflow 说明

请用自然语言描述你的智能体工作流：

- 触发条件（Trigger）
- 决策方式（Evaluate）
- 行动类型（Act）
- 反思机制（Reflect）

> 本实验不追求自动化程度，而关注结构清晰度。

---

## 5. 实验完成情况自评

- [ ] 完成最小可行 Agent（MVA）
- [ ] 设计并执行至少 1 条行动链
- [ ] 有明确的反思记录
```

## 8.3 action.md 模板（行动链设计）

```markdown

# Agent Action Plan


## 1. 行动目标（Goal）

请描述本次 Agent 行动的目标，例如：
- 整理重复概念
- 汇总某一主题知识
- 生成待办或行动建议

---

## 2. 输入与上下文（Context）

- 知识来源（Obsidian 中的哪些笔记）
- 触发方式（手动 / 定期 / 条件触发）

---

## 3. 决策逻辑（Evaluate）

请说明：
- Agent 如何判断“应该做什么”
- 是否生成了多个候选行动
- 是否存在人工确认环节

---

## 4. 行动方式（Act）

- 行动类型：
  - [ ] 只读分析
  - [ ] 建议生成
  - [ ] 人工确认后执行
- 实际执行结果简述

---

## 5. 风险与约束

- 是否存在误操作风险
- 你如何限制 Agent 的行动范围

```

## 8.4 reflection.md 模板（反思与改进）

```markdown
# Agent Reflection

## 1. 本次运行中出现的问题

请描述至少一个问题，例如：
- 决策不清晰
- 行动过于宽泛
- 依赖人工过多

---

## 2. 反思与原因分析

你认为问题的根源是什么？
- 知识结构问题
- 提示设计问题
- 行动链设计问题

---

## 3. 改进方向

如果继续迭代该 Agent，你会：
- 调整哪些结构？
- 增加或删除哪些步骤？
- 如何让 Agent 更稳定？

---

## 4. 一句话总结

> 用一句话总结你对“本地智能体运行环境”的理解。

```

## 8.5 截图要求（screenshots/）

请至少提交以下两张截图：

1. **graph-view.png**

    - Obsidian Graph View

    - 能体现知识节点之间的结构关系

2. **workflow.png**

    - Cherry Studio 中的对话 / 规划 / 行动过程截图

    - 能体现 Agentic Workflow，而非单轮问答

---

## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025 Gitconomy Research社区。
