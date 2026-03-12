# 第七章实验手册指南 — 基于 MCP 的最小化 Agent 实验

> 📌 **实验宗旨**：  本实验的目标是在已有 Agent Runtime 的基础上，引入 MCP Server，跑通一个具备外部能力的最小化 Agent（Minimal Viable Agent, MVA）**。

## 1. 实验目标与学习成果

第七章实验是在 **Lab06 本地优先 Agent Runtime** 之上的一次**能力扩展实验**。

在 Lab06 中，你已经完成了：

- 本地知识环境（Obsidian）
- 单 Agent 的 **PEAR 行动闭环**
- 人机回路的可控执行

<!-- end list -->

在 Lab07 中，你将进一步实现：

1. **理解 MCP 的真实作用位置：** 明确 MCP 不是“另一个工具接口”，而是 **Agent 获取外部能力的协议层**。
2. **跑通最小化 MCP Agent：** 在不破坏本地优先原则的前提下，让 Agent 能够：
    - 调用 1 个 Hosted MCP（来自 ModelScope MCP 广场）
    - 将外部信息纳入决策过程
3. **建立“外部能力 × 本地知识”的协同模式：**  部能力只用于补充信息，本地 Obsidian 仍是唯一事实源。

<!-- end list -->

完成本实验后，你将具备：

- 设计 可扩展 Agent Runtime 的能力
- 判断 什么时候需要 MCP、什么时候不需要 的工程意识
- 为后续“多 Agent / MCP 协作”奠定稳定基础

<!-- end list -->

---

## 2. 实验能力说明：前置要求与学习产出

### 2.1 前置技术能力要求

在开始 Lab07 前，你应已完成并理解：

- **Lab06 全部内容**：
    - PEAR 行动框架
    - 本地优先 Agent Runtime
    - 人机回路执行模式

<!-- end list -->

- [Cherry Studio 基础使用](./../06-Tools/cherry-studio-intallation-guide.md)：
    - 多轮对话
    - 选择 MCP Server

<!-- end list -->

- **Obsidian基础操作**：
    - 笔记阅读与编辑
    - 实验目录管理

<!-- end list -->

### 2.2 核心技能产出

完成 Lab07 后，你将新增以下能力：

|核心技能|对应实验能力|
|---|---|
|MCP 能力定位|能解释 MCP 在 Agent 系统中的作用边界|
|外部能力接入|能通过 Cherry Studio 调用 Hosted MCP|
|最小化 Agent 设计|能设计并运行一个“只用 1 个 MCP”的 Agent|
|信息治理意识|能判断外部信息是否值得写回本地知识库|

---

## 3. 实验准备

### 3.1 学习准备

在开始实验前，请确认你已经理解：

- 为什么不能把所有能力都放进 Agent？
- 为什么外部信息必须经过人工筛选？
- 为什么 MCP 不应直接修改本地知识？

<!-- end list -->

### 3.2 工具与环境准备

|工具|用途定位|
|---|---|
|**Obsidian**|本地知识与状态环境|
|**Cherry Studio**|Agent / MCP Client|
|**ModelScope MCP 广场**|外部能力来源（Hosted MCP）|

请确认：

- Cherry Studio 已安装并可正常使用
- 已按工具手册完成 **MCP Server 同步（Sync Server）**
- 能在对话中选择并启用 MCP Server

<!-- end list -->

### 3.3 实验系统结构说明

本实验的三层结构：

```markdown
┌────────────────────────┐
│ Obsidian Vault         │ ← 运行环境 / 长期记忆 / 状态
│  - 知识                │
│  - 行动结果            │
│  - 反思记录            │
└─────────▲──────────────┘
          │（写回）
┌─────────┴──────────────┐
│ Cherry Studio           │ ← MCP Client / 多 Agent 调度
│  - Planner Agent        │
│  - Executor Agent       │
│  - Critic Agent         │
└─────────▲──────────────┘
          │（协议调用）
┌─────────┴──────────────┐
│ MCP Server              │ ← 外部能力（工具）
│  - 搜索 / 查询 / 计算   │
│  - ModelScope 能力等    │
└────────────────────────┘
```

**关键原则**：

- Obsidian是“事实源”
- MCP Server 不能直接改 Vault
- Agent 只能“建议 + 调用 + 解释”，不能“越权执行”

<!-- end list -->

---

## 4. 实验流程：跑通最小化 MCP Agent

### 4.1 任务说明

本实验统一采用 **PEAR 行动框架**：

|阶段|核心问题|角色定位|
|---|---|---|
|Planning|要解决什么问题？|人|
|Evaluate|是否需要外部能力？|Agent|
|Act|调用 MCP 并执行|人机回路|
|Reflect|是否值得、是否过度|人 + Agent|

在 Lab07 中，你将完成：

1. 明确一个学习型任务（Planning）

2. 让 Agent 判断是否需要 MCP（Evaluate）

3. 至少调用 **1 次 Hosted MCP**（Act）

4. 反思 MCP 的必要性（Reflect）

<!-- end list -->

---

### 4.2 实验文档结构说明

请在你的课程仓库中创建 Lab07 实验目录：

```markdown
📁 01-Labs
└─ 📁 Lab07/
   └─ 01-mcp-agent-run.md
```

本实验 **仅使用一个实验文件**，与 Lab06 保持一致。

---

### 4.3 实验步骤

#### 4.3.1 任务一：Planning —— 明确学习目标

在 `01-mcp-agent-run.md` 中填写：

```markdown
## Planning

**目标（Goal）**：
- 如何学习生成式思维与知识工作流？

**作用范围（Scope）**：
- 涉及：课程讲义 + 1 条外部资料
- 不涉及：额外工具、自动写回

**完成标准（Done Criteria）**：
- 形成一份结构化学习路径说明
```

#### 4.3.2 任务二：Evaluate —— 判断是否需要 MCP

在 Cherry Studio 中输入：

```markdown
你是一个智能体规划器。
请基于以下 Planning：
1. 给出学习生成式思维与知识工作流的行动计划
2. 标注哪一步需要调用外部资料（MCP）
3. 不要自动执行
```

将结果写入：

```markdown
## Evaluate
- Step 1:
- Step 2: （需要 MCP）
- Step 3:
```

#### 4.3.3 任务三：Act —— 调用 MCP（人机回路）

1. 在 Cherry Studio 对话中启用 **ModelScope Hosted MCP**
2. 让 Agent 获取一条外部资料要点
3. **人工筛选后**，将要点写入实验文件：

<!-- end list -->

```markdown
## Act
- [x] 调用 MCP 获取外部资料
- [x] 人工筛选并整理为学习要点
```

#### 4.3.4 任务四：Reflect —— 反思 MCP 的使用

```markdown
## Reflect
- MCP 是否必要？
- 哪些信息其实可以只靠本地知识？
- 下次是否可以减少 MCP 调用？
```

---

## 5. 实验成果提交方式

### 5.1 统一提交根目录

所有实验成果请统一提交至：`08-Workspace/Assignment-M06/`，在提交根目录下，请按 **小组 → 个人** 两级目录组织成果

目录结构：

```markdown
📁 08-Workspace/Assignment-M07/
└─ 📁 Group-A/
   └─ 📁 YourName/
      └─ 01-mcp-agent-run.md
```

### 5.2 Pull Request 作业提交流程（正式提交）

当小组组员完提交后，需由 **组长** 提交最终 PR。
#### 5.2.1 步骤 1：Commit 规范

Commit message：

2. `git commit -m '[M07]`YouName`提交Lab05实验文件'`

#### 5.2.2 步骤 2：Push 至队长仓库

1. `git push origin main`

#### 5.2.3 步骤 3：Pull Request到主仓库

PR标题规范：

1. `GroupName`提交第七章实验成果`

PR 内容须包含：

1. `- 文件路径`
2. `- 本次更新摘要`

#### 5.2.4 步骤4：等待讲师Review → Merge

讲师/助教会进行审核并给予意见。

🎉 **恭喜你完成 Lab07！**

你已经成功跑通了一个在本地知识环境中、通过 MCP 协议安全获取外部能力的最小化 Agent。

---

## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025 Gitconomy Research社区。
