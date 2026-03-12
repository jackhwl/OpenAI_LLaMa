# 第四章实验手册指南 ：构建智能知识系统的工程化基座

> 📌 **实验宗旨**：将个人知识库从“静态文本”重构为“智能资产”。通过引入 Git 工作流、YAML 元数据架构及 Agentic Workflow（代理式工作流），实现知识的可版本化、机器可读与自主迭代。

## 1. 实验目标与学习成果

本实验将引导你从零开始，应用软件工程的方法论来重构你的个人知识库。你将不再把笔记仅仅看作文本，而是将其视为“代码”。

完成本实验后，你将能够：

1. **实践“知识即代码”**：利用 Git 建立规范的协作范式，通过功能分支与原子提交追踪思维迭代。
2. **构建机器友好的数据层**：设计面向 RAG 优化的 YAML 元数据，实现知识的原子化拆分与合成问题生成。
3. **设计人机协作协议**：应用 S.C.O.R.E 模型定义思维接口，实现高确定性的提示工程。
4. **运行代理式工作流**：手动模拟“规划-工具-反思”循环，理解自主智能体的运行机制。

---

## 2. 实验能力说明：前置要求与学习产出

### 2.1 前置技术能力要求

- **Git 基础**：具备基础的 Git 命令行操作能力（init, commit, branch, merge）。
- **工具基础**：已完成Lab01-03，熟练使用Obsidian进行知识管理。
- **认知基础**：理解 RAG（检索增强生成）的基本原理。

### 2.2 核心技能产出

- **工程层**：掌握功能分支工作流（Feature Branch Workflow）与 Conventional Commits 规范。
- **数据层**：能够为笔记配置 UUID、Aliases、Related Questions 等元数据字段。
- **代理层**：掌握 ReAct 模式（Reasoning and Acting）的闭环设计。

---

## 3. 实验准备

### 3.1 学习准备

- 已完成 **第四章（Module 04）** 学习，理解“知识即代码”的隐喻。
- 理解 RAG 检索中“分块（Chunking）”与“召回率（Recall）”的关系。

### 3.2 工具与环境准备

- **Obsidian**：用于元数据编辑与可视化。
- **Git 客户端**：用于版本控制实战。
- **LLM 访问**：具备多轮对话能力，模拟 Agent 环境。

---

## 4. 实验流程：重构知识引擎

## 4.1 任务说明

本实验围绕第四章讲义中提出的 “智能知识工程（Intelligent Knowledge Engineering）” 展开，目标不是生成更多内容，而是将已有知识转化为可被系统持续使用、协作维护与智能调用的工程资产。

在本实验中，你将完成以下三项核心任务：

1. **将知识视为工程资产（Knowledge as Code）：**  在既有 Obsidian Vault 中创建或扩展知识笔记，使其成为可维护、可复用的长期资产。

2. **为知识添加结构化语义与元数据：** 通过 YAML Frontmatter、标签与原子化内容拆分，使知识不仅“可读”，而且“可被系统理解”。

3. **为后续智能体与 RAG 场景做好准备：** 所有实验产出需面向未来的检索、组合与代理运行，而非仅服务于当前一次实验。

本实验重点考察：

1. 知识是否被结构化、沉淀并可持续维护
2. 你是否开始以“系统视角”看待生成式 AI
3. 实验产出是否能够自然承接后续的 RAG / Agent 场景

## 4.2 实验文档结构说明

1. 在Obidian Valut创建Lab03目录
2. 本章实验的文档结构

```markdown
📁 AI-Knowledge-Workflow-Course
├─ 📁 01-Labs
│  └─ 📁 Lab04/
│      │─ 01-score-prompt.md
│ 	   │─ 02-score-run.md
│ 	   │─ 03-critic-prompt.md
│ 	   │─ 03-critic-run.json
│      │─ 04-refined-prompt.md
│      │─ 05-refined-run.md
│      │─ 06-agent-plan.md
│      │─ 07-agent-executor-output
│      └─ 08--agent-reflection
├─ 📁 02-Knowledge
│     └─ rag-concepts.md
├─ 📁 03-Screenshot
│     └─ lab04-canvas.png
└─ 📁 05-Output
      └─ lab04-report.md
```

---

## 4.3 实验步骤
### 4.3.1 任务一：知识即代码——Git 工作流实战

> 📌 **理论对应**：讲义 4.1.2（功能分支工作流） & 4.1.4（提交信息规范）

在前序实验中，你已经学会将 Prompt、Schema 与日志保存为结构化文档。  
本任务的目标，是引入 **Git 的工作流视角**，帮助你理解当知识被视为“代码”时，它应当如何被修改、记录与协作维护。

请注意：  本任务的重点不是掌握复杂的 Git 技巧，  而是体会 Git 所代表的三种工程思想：  **版本、变更与协作**。

完成本任务后，你应当能够：

- 将一条知识笔记视为可版本化的工程资产
- 使用 Git 的“提交”来记录一次明确的认知变更
- 理解协作场景下“谁在什么时间、做了什么修改”

#### 4.3.2.1 步骤1：选择或创建一条知识笔记

在 `02-Knowledge/` 目录下，选择一条知识笔记作为实验对象，例如 `02-Knowledge/rag-concepts.md`）

```markdown
# RAG（Retrieval-Augmented Generation）核心概念

## 1. 概念定义（What）

**RAG（Retrieval-Augmented Generation，检索增强生成）**  是一种将 **外部知识检索（Retrieval）** 与 **大语言模型生成（Generation）** 相结合的工作范式。

其核心思想是：  
> 📌 在生成回答之前，先从可控的知识库中检索相关信息，再将检索结果作为上下文提供给模型，从而提升回答的**准确性、可控性与可追溯性**。

---

## 2. 为什么需要RAG（Why）

在纯生成式模型（纯Prompt）中，常见问题包括：

- ❌ **幻觉（Hallucination）**：模型生成不存在或不准确的信息  
- ❌ **知识不可控**：无法确定模型“依据了什么”作答  
- ❌ **知识更新困难**：模型参数更新成本高  

RAG通过“**先查再答**”的方式，显著缓解上述问题。

---

## 3. 基本工作流程（How）

一个最小可行的 RAG 工作流通常包含以下步骤：

1. **Query 构造**：将用户问题转化为可检索的查询
2. **Retrieval**：从向量库 / 文档库中检索相关内容
3. **Context 拼接**：将检索结果整理为上下文
4. **Generation**：将上下文 + Prompt 输入给 LLM 生成回答

> 📌 在课程中，这一流程通常映射为：  
> **Input → Structure → Generate → Iterate → Express（I-S-G-I-E）**

---

## 4. RAG的核心价值（Value）

- **降低幻觉风险**：答案基于真实文档
- **增强可解释性**：可追溯“答案来源”
- **支持快速更新**：更新知识库 ≠ 重新训练模型
- **工程友好**：适合集成到业务系统与 Agent

---

## 5. RAG与Prompt的关系

| 对比维度 | 纯 Prompt | RAG |
|--------|----------|-----|
| 知识来源 | 模型内隐知识 | 外部显式知识 |
| 可控性 | 低 | 高 |
| 可更新性 | 低 | 高 |
| 工程可维护性 | 弱 | 强 |

>📌  可以将 Prompt 理解为**“如何说”**，  而 RAG 解决的是**“基于什么说”**。

---

## 6. 企业级应用场景（Where）

- 企业内部知识问答（制度 / 文档 / 规范）
- 行业报告与研究辅助生成
- 客服与技术支持系统
- 智能体（Agent）的知识底座

---

## 7. 当前挑战与注意事项（Limits）

- 检索质量直接影响生成质量
- Chunk 切分策略需要精心设计
- 上下文长度与成本需权衡
- 不等同于“万能正确”，仍需评价机制

---

## 8. 与后续章节的关系（Course Mapping）

- **第二章**：MVW —— 跑通最小工作流
- **第三章**：结构化协议 —— 控制输出熵
- **第四章**：知识即代码 —— 版本化与协作
- **第五章**：RAG / GraphRAG —— 系统级知识组织
- **第七章**：Agent —— RAG 成为行动决策的一部分

---

## 9. 修改记录（Version Notes）

- v0.1：初始定义与基础流程说明  
- v0.2：补充企业应用场景与课程映射说明

```

#### 4.3.2 步骤2：Git 工作流初始化

这一步的目标不是学习 Git 命令本身， 而是将当前的 Obsidian Vault  从“个人笔记空间”正式转变为可追溯、可演进的知识工程仓库。

1. **执行Git仓库初始化：**

进入AI-Knowledge-Workflow-Course的目录，执行`git init`，该命令会在当前目录中创建一个 Git 仓库，用于记录后续所有知识变化。

```bash
git init

hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint:
hint: 	git config --global init.defaultBranch <name>
hint:
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint:
hint: 	git branch -m <name>
```

出现以上的提示先是Git 的正常提示信息，不是错误。

2. **创建Git仓库主分支**

```bash
git branch -M main
git status

On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.obsidian/
	00-Inbox/
	01-Labs/
	02-Knowledge/
	04-Screenshot/
	Welcome.md
```

#### 4.3.3 步骤3：创建基线提交（Baseline Commit）

在开始创建或修改任何知识文件之前，  请先对当前 Vault 状态进行一次**基线提交**：

```bash
git add .
git commit -m "chore: initialize knowledge workspace"

[main (root-commit) 87d6da5] chore: initialize knowledge workspace
 26 files changed, 860 insertions(+)
 create mode 100644 .obsidian/app.json
 create mode 100644 .obsidian/appearance.json
 create mode 100644 .obsidian/core-plugins.json
 create mode 100644 .obsidian/graph.json
 create mode 100644 .obsidian/workspace.json
 create mode 100644 00-Inbox/news-01.md
 create mode 100644 00-Inbox/structured-run-1.json
 create mode 100644 00-Inbox/structured-run-2.json
 create mode 100644 00-Inbox/structured-run-3.json
 create mode 100644 01-Labs/Lab01/guohao-lab01-log.md.md
 create mode 100644 01-Labs/Lab02/guohao-lab02-mvw.md
 create mode 100644 01-Labs/Lab03/01-prompt-unstructured.md
 create mode 100644 01-Labs/Lab03/02-unstructured-run.md
 create mode 100644 01-Labs/Lab03/03-prompt-structured.md
 create mode 100644 01-Labs/Lab03/04-judge-prompt.md
 create mode 100644 01-Labs/Lab03/05-refine-prompt.md
 create mode 100644 01-Labs/Lab03/06-final-prompt.md
 create mode 100644 01-Labs/Lab03/07-schema.json
 create mode 100644 01-Labs/Lab03/08-structured-run.json
 create mode 100644 01-Labs/Lab03/09-validator.py
 create mode 100644 01-Labs/Lab03/10-refine-run.json
 create mode 100644 01-Labs/Lab03/lab03-system.canvas.canvas
 create mode 100644 01-Labs/Lab04/lab04-log.md
 create mode 100644 02-Knowledge/rag-concepts.md.md
 create mode 100644 04-Screenshot/lab03-obsidian-canvas.png
 create mode 100644 Welcome.md

```

这次提交的意义是：

- 标记 **“知识工程正式开始前的初始状态”**
- 为后续每一次知识演化提供对照基准

### 4.3.2 任务二：数据层构建——面向 RAG 的元数据设计

> 📌 **理论对应**：讲义 4.2.1（YAML Frontmatter） & 4.2.2（原子化与合成问题）

在上一任务中，你已经完成了**知识文本本身的工程化管理**（Git + Markdown）。  但仅有“可读的文本”，还不足以支撑 **RAG / Agent 系统的自动检索与组合**。

本任务的目标是为知识增加“机器可理解的外壳”， 让它不仅能被人阅读，也能被系统检索、筛选与组合。在本课程中，我们使用 **YAML Frontmatter** 作为元数据载体，原因是：

- 它与 Markdown 天然融合
- 人类可读、机器可解析
- 易于版本控制与协作维护


YAML Frontmatter 并不是“给模型看的 Prompt”，  而是给系统看的“知识标签与结构说明”**。

#### 4.3.2.1 步骤 1：定义YAML Schema

在 `rag-concepts.md` 文件顶部，插入`YAML Frontmatter`r 示例（可按需微调）。你需要严格按照讲义 4.2.1 的建议，包含以下字段：


```yaml
---
uuid: [使用工具生成一个UUID，或手动填一个唯一码]
type: Concept
domain: ai-architecture
topic: rag
tags:
  - RAG
  - Retrieval
  - Knowledge-Engineering
use_cases:
  - enterprise-qa
  - agent-knowledge-base
status: Seedling
visibility: Public
related_questions:
  - 什么是RAG技术？
  - RAG如何解决大模型的幻觉问题？
---
```

YAML Frontmatter 字段说明（面向 RAG / 知识工程）

| **字段名**             | **示例值**                                        | **作用说明（教学向）**                                                                           |
| ------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------- |
| `uuid`              | `c3a9b2e4-7f1d-4a9e-9d3b-8c2f0a1e7c11`         | **全局唯一标识符**。用于在 RAG / GraphRAG / 多 Agent 系统中稳定引用该知识节点，避免因文件名或路径变化导致引用失效。推荐使用工具生成，保证唯一性。 |
| `type`              | `Concept`                                      | **知识类型标识**。用于区分“概念 / 方法 / 案例 / 规范”等不同知识形态，帮助系统或 Agent 在组合知识时采用不同处理策略。                   |
| `domain`            | `ai-architecture`                              | **所属领域**。用于跨领域筛选与限定检索范围，例如只在“AI 架构”或“数据工程”域内召回知识。                                       |
| `topic`             | `rag`                                          | **核心主题锚点**。通常为单一、稳定的主题关键词，用于快速定位该知识解决的“是什么问题”。                                          |
| `tags`              | `RAG`, `Retrieval`, `Knowledge-Engineering`    | **多维标签集合**。提供比 `topic` 更灵活的检索入口，支持组合查询（如 `RAG + Knowledge-Engineering`）。                |
| `use_cases`         | `enterprise-qa`, `agent-knowledge-base`        | **使用场景声明**。明确该知识在什么任务或系统中会被使用，是 RAG / Agent 进行“是否调用该知识”判断的重要依据。                         |
| `status`            | `Seedling`                                     | **知识成熟度状态**。`Seedling` 表示“早期/待验证知识”，区别于 `Stable` 或 `Deprecated`，用于避免系统在关键任务中误用不成熟内容。    |
| `visibility`        | `Public`                                       | **可见性控制**。区分公开知识与内部/私有知识，为后续权限控制或多知识库场景预留接口。                                            |
| `related_questions` | 见示例                                            | **关联问题列表**。用于引导检索、问答与教学，也可直接作为 RAG 的 Query 模板或 Agent 的问题触发器。                            |

>📌 YAML Frontmatter 是知识进入 RAG / Agent 系统之前，必须穿上的“工程外壳”

#### 4.3.2.2 步骤 2：原子化拆分与问题生成

将rag-concept.md 让 LLM 为每个知识点生成 2-3 个用户查询问题，存入 `related_questions`

1. **准备输入文本：**

选取其中一个**明确的小节**（例如：`## 为什么需要 RAG`），  作为本次原子化与问题生成的输入。

2. **让 LLM 生成原子陈述：**

将该小节正文复制给 LLM，并使用如下提示语：

```markdown
请将以下文本拆解为若干条“原子化知识陈述”。

要求：
1. 每条陈述只表达一个明确事实或观点
2. 陈述之间相互独立，不依赖上下文
3. 不要解释，只输出列表形式

【输入文本】
<<<TEXT
## 2. 为什么需要RAG（Why）

在纯生成式模型（纯Prompt）中，常见问题包括：

- ❌ **幻觉（Hallucination）**：模型生成不存在或不准确的信息  
- ❌ **知识不可控**：无法确定模型“依据了什么”作答  
- ❌ **知识更新困难**：模型参数更新成本高  

RAG通过“**先查再答**”的方式，显著缓解上述问题。
TEXT

```

你将得到类似结果（示例）：

```markdown
1.  纯生成式模型存在知识不可控的问题。
2.  知识不可控指无法确定模型“依据了什么”作答。
3.  纯生成式模型存在知识更新困难的问题。
4.  知识更新困难是因为模型参数更新成本高。
5.  RAG通过“先查再答”的方式工作。
6.  RAG能显著缓解纯生成式模型的上述常见问题。
```

3. **请将生成的用户查询问题，整理并写入知识文件中。**

在`rag-Concepts.md` 的YAML Frontmatter补充：

```yaml
related_questions:   
- 什么是RAG技术？  
- RAG如何解决大模型的幻觉问题？
- 纯生成式模型存在知识不可控的问题。
- 知识不可控指无法确定模型“依据了什么”作答。
- 纯生成式模型存在知识更新困难的问题。
- 知识更新困难是因为模型参数更新成本高。
- RAG通过“先查再答”的方式工作。
- RAG能显著缓解纯生成式模型的上述常见问题。
---
```

### 4.3.3 任务三：知识切分与 Chunk 策略（向量化前准备）

> 📌 **理论对应**：讲义 4.2.2（原子化与合成问题）、讲义 4.2.3（从文档到可计算知识单元）& 讲义 4.2.4（检索粒度与上下文命中率）

在前两个任务中，你已经完成了知识的工程化管理与元数据标注。本任务的目标是解决进入 RAG 系统前的粒度问题：一篇知识文档，应该以什么粒度被系统“记住”并提取？。

本任务的实验目标：

- **消除语义碎片化**：通过结构化设计，避免传统固定长度切分（Fixed-size Chunking）导致的语义断裂。
- **实现独立可理解性**：确保每个知识分块（Chunk）在脱离全文时仍具备完整的逻辑信息。

Chunk 化结构不是“切分文本”，而是“把隐含的问题显性化”。换句话说：每一个 `##`，本质上都是一个“系统应该单独回答的问题”。Chunk化不是从 Markdown开始，而是从「问题空间」开始。

#### 4.3.3.1 步骤1：先“拆问题”，再“拆文本”

生成一个结构化的Prompt ，利用LLM对`rag-concept.md`的Chunk策略进行评估

```
请你阅读以下文档，完成以下任务：

1. 列出文档中隐含回答的所有核心问题
2. 确保每个问题都可以独立成立
3. 按问题重组文档结构，使每个二级标题只回答一个问题
4. 重组后的每个小节必须在脱离全文时仍可被理解

【输入文档】
<<<TEXT
（粘贴 rag-concepts.md 原文）
TEXT
```

LLM的反馈示例：

```markdown
**文档隐含回答的核心问题列表：**

1.  RAG 是什么？（What）
2.  为什么需要 RAG？（Why）
3.  RAG 是如何工作的？（How）
4.  RAG 能带来什么核心价值？（Value）
5.  RAG 与纯 Prompt 方法有何不同？（Comparison）
6.  RAG 适用于哪些企业场景？（Where/Application）
7.  RAG 当前面临哪些挑战与注意事项？（Challenges）
8.  RAG 技术有哪些发展方向？（Future）

**按问题重组后的文档结构：**

# RAG（检索增强生成）核心概念解读

## 1. RAG是什么？（What）
RAG（Retrieval-Augmented Generation，检索增强生成）是一种将 **外部知识检索** 与 **大语言模型生成** 相结合的工作范式。其核心思想是：在生成回答之前，先从可控的知识库中检索相关信息，再将检索结果作为上下文提供给模型，从而提升回答的**准确性、可控性与可追溯性**。

## 2. 为什么需要RAG？（Why）
在纯生成式模型（纯Prompt）中存在以下主要问题：**幻觉**（生成不存在或不准确的信息）、**知识不可控**（无法确定作答依据）、**知识更新困难**（模型参数更新成本高）。RAG通过“**先查再答**”的方式，能显著缓解上述问题。

## 3. RAG是如何工作的？（How）
一个最小可行的 RAG 工作流包含四个步骤：1) **Query 构造**：将用户问题转化为可检索的查询；2) **Retrieval**：从向量库或文档库中检索相关内容；3) **Context 拼接**：将检索结果整理为上下文；4) **Generation**：将上下文与提示词一同输入给大语言模型以生成最终回答。

## 4. RAG能带来什么核心价值？（Value）
RAG的核心价值体现在四个方面：**降低幻觉风险**（答案基于真实文档）、**增强可解释性**（可追溯答案来源）、**支持快速更新**（仅更新知识库，无需重新训练模型）、**工程友好**（适合集成到业务系统与智能体中）。

## 5. RAG与纯Prompt 方法有何不同？（Comparison）
RAG与纯Prompt的关键区别在于：RAG的**知识来源**是外部显式知识，而纯Prompt依赖模型内隐知识；RAG在**可控性**、**可更新性**和**工程可维护性**方面均优于纯Prompt。简言之，Prompt解决“如何说”，而RAG解决“基于什么说”。

## 6. RAG适用于哪些企业场景？（Where/Application）
RAG适用于多种企业级场景，主要包括：企业内部知识问答（如制度、文档查询）、行业报告与研究辅助生成、客服与技术支持系统，以及作为智能体（Agent）的知识底座。

## 7. RAG当前面临哪些挑战与注意事项？（Challenges）
应用RAG时需注意：**检索质量直接影响生成质量**；文档的**分块（Chunk）策略需要精心设计**；需要权衡**上下文长度与成本**；RAG不等同于“万能正确”，仍需建立相应的**评价机制**。

## 8. RAG技术有哪些发展方向？（Future）
RAG技术正朝着更系统的知识组织（如GraphRAG）发展，并日益成为智能体进行行动决策的核心组成部分，这代表着其从问答工具向复杂系统“知识底座”演进的方向。

```


为什么这个重组结果满足 Chunk 设计要求？

|Chunk 设计原则|是否满足|说明|
|---|---|---|
|一 Chunk 一问题|✅|每个 `##` 对应一个明确问题|
|可独立理解|✅|任意小节脱离全文仍成立|
|可被系统调用|✅|可直接作为 Prompt 上下文|
|向量化友好|✅|语义边界清晰、无跨段依赖|
#### 4.3.3.2 步骤2：元数据增强

将生成的“合成问题”植入YAML元数据中。这些问题充当该文档在向量空间中的“语义锚点”，用于提升检索召回率。

增强后的YAML元数据示例：

```yaml
---
uuid: 550e8400-e29b-41d4-a716-446655440000
type: Concept
domain: ai-architecture
topic: rag
tags:
  - RAG
  - Retrieval
  - Knowledge-Engineering
  - LLM
use_cases:
  - enterprise-qa
  - agent-knowledge-base
  - report-generation
status: Seedling
visibility: Public
related_questions:
  - 什么是RAG？
  - RAG的核心思想是什么？
  - 为什么纯Prompt模式容易产生幻觉？
  - RAG如何缓解大模型的幻觉问题？
  - 一个最小可行的RAG工作流程包含哪些步骤？
  - RAG相比纯Prompt的工程优势体现在哪里？
  - Prompt与RAG各自解决什么问题？
  - RAG在企业级场景中通常用在哪里？
  - RAG在工程实践中面临哪些挑战？
---
```

#### 4.3.3.3 步骤3：物理结构重构

调整正文结构，确保每一个二级标题（`##`）对应一个潜在的知识分块（Chunk），并消除跨段落的指代模糊。

`rag-concepts.md `全文样例（正文重构）：

```markdown
---
uuid: 550e8400-e29b-41d4-a716-446655440000
type: Concept
domain: ai-architecture
topic: rag
tags:
  - RAG
  - Retrieval
  - Knowledge-Engineering
  - LLM
use_cases:
  - enterprise-qa
  - agent-knowledge-base
  - report-generation
status: Seedling
visibility: Public
related_questions:
  - 什么是RAG？
  - RAG的核心思想是什么？
  - 为什么纯Prompt模式容易产生幻觉？
  - RAG如何缓解大模型的幻觉问题？
  - 一个最小可行的RAG工作流程包含哪些步骤？
  - RAG相比纯Prompt的工程优势体现在哪里？
  - Prompt与RAG各自解决什么问题？
  - RAG在企业级场景中通常用在哪里？
  - RAG在工程实践中面临哪些挑战？
---

# 检索增强生成（RAG）核心概念

## 什么是 RAG（What）

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将**外部知识检索机制**
与**大语言模型生成能力**相结合的工作范式。

RAG 的目标是在生成回答之前，引入来自知识库、文档集或数据库的相关信息，
并将这些信息作为上下文输入给模型，从而提升生成结果的准确性与可控性。

---

## RAG 的核心思想是什么（Principle）

RAG 的核心思想可以概括为一句话：

> **在生成回答之前，先从可控的知识源中检索相关信息。**

通过这种“先查再答”的方式，模型的输出不再完全依赖其内隐参数，
而是建立在外部、可维护、可追溯的知识基础之上。

---

## 为什么需要 RAG（Why）

在仅依赖 Prompt 的纯生成式模型中，工程实践常见以下问题：

- **幻觉问题**：模型可能生成不存在或不准确的信息  
- **知识不可控**：难以判断模型回答所依据的来源  
- **知识更新成本高**：更新知识通常需要重新训练或微调模型  

这些问题在企业级应用中尤为突出。

---

## RAG 是如何缓解这些问题的（Mechanism）

RAG 通过在生成阶段之前引入外部知识检索，使模型回答基于真实文档，
从而在工程层面实现以下改进：

- 回答基于检索到的文档，降低幻觉风险  
- 检索结果可作为证据，提高结果可解释性  
- 知识更新转移到知识库层面，而非模型参数层面  

---

## RAG 的基本工作流程（How）

一个最小可行的 RAG 工作流程通常包含以下步骤：

1. **Query 构造**：将用户问题转化为可检索的查询  
2. **Retrieval**：从向量库或文档库中检索相关内容  
3. **Context 拼接**：整理检索结果，构建上下文  
4. **Generation**：将上下文与 Prompt 一同输入给模型生成回答  

在本课程中，该流程通常映射为：

> **Input → Structure → Generate → Iterate → Express（I–S–G–I–E）**

---

## RAG 的核心工程价值（Value）

从工程角度看，RAG 的核心价值体现在以下方面：

- **降低幻觉风险**：答案基于真实文档  
- **增强可解释性**：可追溯生成所依赖的知识来源  
- **支持快速更新**：更新知识库无需重新训练模型  
- **工程友好**：适合集成到业务系统与 Agent 架构中  

---

## RAG 与 Prompt 的关系（Comparison）

Prompt 主要解决的是 **“如何让模型表达”** 的问题，
而 RAG 解决的是 **“模型基于什么知识进行表达”** 的问题。

二者并非替代关系，而是协作关系：
Prompt 定义表达方式，RAG 提供事实基础。

---

## RAG 的企业级应用场景（Where）

RAG 常见于以下企业级应用场景：

- 企业内部知识问答系统（制度、规范、文档）  
- 行业研究与报告辅助生成  
- 客服与技术支持系统  
- 智能体（Agent）的长期知识记忆模块  

---

## RAG 的挑战与注意事项（Limits）

尽管 RAG 能显著提升生成质量，但在工程实践中仍需注意：

- 检索质量直接影响最终回答质量  
- Chunk 粒度设计不当会引入噪声  
- 上下文长度与推理成本需要权衡  
- RAG 仍需要评价与反馈机制进行校验  

---

## 本知识在课程体系中的位置（Course Mapping）

本知识在《生成式思维与知识工作流》课程中的位置如下：

- **第二章**：最小可行工作流（MVW）  
- **第三章**：结构化协议与输出控制  
- **第四章**：知识即代码与智能知识工程  
- **第五章**：RAG / GraphRAG 的系统实现  
- **第七章**：Agent 中的知识调用与决策  

---

## 修改记录（Version Notes）

- **v0.1**：初始定义与基础流程说明  
- **v0.2**：补充企业应用场景与课程映射  
- **v0.3**：按 Chunk 设计原则重构全文结构

```

#### 4.3.3.4 步骤 4：关联性标注

在完成 **Chunk 级结构重构** 之后，每一个知识块已经可以被 **“单独检索”**。  
但在真实的 RAG / Agent 系统中，仅有“孤立的 Chunk”还不够，系统还需要知道：

> 📌 **这些知识之间，存在什么关系？**

本步骤的目标，是通过显式的双向链接（`[[ ]]`）， 为后续 GraphRAG/Agent 推理提供可解析的知识网络结构。

在本课程中，**关联性标注 ≠ 自然语言引用**，而是：

- 使用 `[[概念名]]` 明确声明 **“这个 Chunk 依赖 / 指向 / 扩展了哪个概念”**
- 让系统可以从文本中直接抽取 **节点（Node）与边（Edge）**
- 为 GraphRAG、知识图谱、Agent Planning 提供结构基础

在 Lab04 中，我们重点关注三类关联（**不需要全部用上**）：

1. **概念关联**：一个概念依赖另一个概念
2. **流程关联**：一个 Chunk 对应某个流程或阶段
3. **课程关联**：知识在课程体系中的前后位置

基于 `rg-concepts.md` 的具体示例：

```markdown
---
uuid: 550e8400-e29b-41d4-a716-446655440000
aliases:
  - 检索增强生成
  - Retrieval-Augmented Generation
  - RAG
type: Concept
domain: ai-architecture
topic: rag
tags:
  - RAG
  - Retrieval
  - Knowledge-Engineering
  - LLM-Engineering
use_cases:
  - enterprise-qa
  - agent-knowledge-base
status: Seedling
visibility: Public
related_questions:
  - 什么是 RAG 技术？
  - RAG 的核心思想是什么？
  - 为什么纯 Prompt 模型容易产生幻觉？
  - RAG 如何解决知识不可控问题？
  - RAG 的基本工作流程包含哪些步骤？
  - RAG 与 Prompt Engineering 有什么区别？
  - RAG 在企业中有哪些典型应用场景？
  - 使用 RAG 时需要注意哪些工程问题？
---

# 检索增强生成（RAG）

## 1. 什么是 RAG？（What）

**检索增强生成（Retrieval-Augmented Generation，[[RAG]]）**  
是一种将**外部知识检索（[[Retrieval]]）**与**大语言模型生成（[[Generation]]）**相结合的知识处理范式。

在 RAG 中，模型并非仅依赖自身参数进行回答，而是在生成之前，
先从一个**可控、可更新的知识源**中检索相关内容，
再将检索结果作为上下文输入给模型完成生成。

这一机制使生成结果具备更高的**准确性、可控性与可追溯性**。

---

## 2. 为什么需要 RAG？（Why）

在仅依赖 Prompt 的纯生成式模型中，常见工程问题包括：

- **[[幻觉问题]]**：模型可能生成不存在或不准确的信息  
- **[[知识不可控]]**：无法确认模型回答基于哪些事实  
- **[[知识更新成本高]]**：更新知识通常需要重新训练或微调模型  

[[RAG]] 通过“**先检索、再生成**”的机制，
将回答锚定在外部文档之上，从工程层面显著缓解上述问题。

---

## 3. RAG 的基本工作流程是什么？（How）

一个最小可行的 [[RAG]] 工作流程通常包含以下阶段：

1. **Query 构造**：将用户问题转化为可检索的查询表达  
2. **Retrieval**：从向量库或文档库中检索相关内容  
3. **Context 拼接**：将检索结果整理为模型可理解的上下文  
4. **Generation**：将上下文与 Prompt 一并输入给 LLM 生成回答  

在本课程中，该流程被抽象为 [[I-S-G-I-E 知识工作流]]，
用于指导从输入到输出的完整生成路径设计。

---

## 4. RAG 的核心价值是什么？（Value）

从工程与系统视角看，[[RAG]] 具备以下核心价值：

- **降低幻觉风险**：回答基于真实文档而非纯模型猜测  
- **增强可解释性**：可追溯“答案来自哪些文档 Chunk”  
- **支持快速更新**：更新知识库 ≠ 重新训练模型  
- **工程友好**：适合集成到业务系统与 [[Agent 决策系统]]  

这些特性使 RAG 成为企业级 AI 系统中的关键基础组件。

---

## 5. RAG 与 Prompt Engineering 的关系是什么？

[[Prompt Engineering]] 主要解决的是：

> **“模型应该如何表达与思考？”**

而 [[RAG]] 解决的是：

> **“模型基于什么事实与知识作答？”**

二者并非替代关系，而是**分工协作**：

- Prompt 决定 **生成方式**
- RAG 决定 **知识来源**

在工程实践中，稳定系统通常需要二者协同使用。

---

## 6. RAG 的典型应用场景有哪些？（Where）

[[RAG]] 常被应用于以下场景：

- 企业内部知识问答（制度 / 文档 / 规范）
- 行业研究与报告辅助生成
- 客服与技术支持系统
- [[Agent]] 的长期记忆与知识底座  

在这些场景中，RAG 主要承担“**可信知识供给层**”的角色。

---

## 7. 使用 RAG 时需要注意哪些挑战？（Limits）

尽管 [[RAG]] 提供了显著优势，但仍存在关键工程挑战：

- **检索质量决定生成上限**
- **Chunk 切分策略影响召回精度**
- **上下文长度与推理成本需要权衡**
- **仍需评价与反馈机制避免错误累积**

因此，RAG 并不是“自动正确”，而是一种**可被工程化管理的改进路径**。

---

## 8. RAG 在课程体系中的位置是什么？（Course Mapping）

在《生成式思维与知识工作流》课程中，[[RAG]] 位于承上启下的位置：

- 基于 [[MVW]] 跑通最小生成闭环  
- 承接 [[结构化协议]]，实现低熵输出  
- 为 [[GraphRAG]] 与 [[Agent 决策系统]] 提供知识基础  

它是从“文本生成”迈向“系统级智能”的关键中间层。

---

## 9. 修改记录（Version Notes）

- v0.1：概念定义与基础流程说明  
- v0.2：补充工程价值、应用场景与课程映射  

```
使用说明：

- 每一个 `##` = **一个独立 Chunk**
- 任意小节可直接复制进 Prompt 作为上下文
- `[[ ]]` 可被 Obsidian / GraphRAG / Agent 系统解析为知识图
- `related_questions` 可直接作为 RAG Query 或教学提问集

---

### 4.3.4 任务四：交互层设计——编写 S.C.O.R.E协议

> 📌 **理论对应**：讲义 4.3.1（S.C.O.R.E 模型）与 讲义 2.4（S.C.O.R.E 详解）

在前三个任务中，你已经完成了：

1. **知识层**：将 RAG 相关知识以 Chunk 形式进行结构化组织
2. **数据层**：通过 YAML Frontmatter 与 Chunk 设计，使知识可被系统检索
3. **切分层**：确保每一个 Chunk 都能独立进入检索与生成流程


但到目前为止，这些知识**仍然只是“被存储”，尚未被“稳定调用”**。

本任务要解决的是一个关键的工程问题：系统或智能体，应当如何“正确地向模型提问”，才能稳定、可复用地调用这些知识？

为此，我们引入 S.C.O.R.E协议，作为**人—模型—知识之间的交互层规范**。

完成本任务后，你应当能够：

- 将一次自然语言提问，重构为结构化、可复用的 Prompt 协议
- 明确 Prompt 中角色、背景、目标、约束与评价标准
- 编写一份可直接用于 RAG / Agent 系统的 S.C.O.R.E Prompt 模板

#### 4.3.4.1 步骤1：从自然提问到协议化交互

**原始自然语言提问（示例）**：

```markdown
请你介绍一下什么是RAG，它有什么用？
```

问题在于：

- 没有角色设定（模型不知道自己是谁）
- 没有输出边界（长度、结构不确定）
- 没有评价标准（系统无法判断好坏）

#### 4.3.4.2 步骤2：编写 S.C.O.R.E 协议（示例）

编辑`01-score-prompt.md`，写入如下内容（示例模板）：


```markdown
## 1. Setting（角色设定）

你是一个“知识调用与解释模块”，  
工作在一个需要**稳定、可复用、可校验输出**的智能知识系统中。

你的职责不是自由发挥，也不是补充外部常识，  
而是**严格基于我提供的知识 Chunk 进行回答**。

---

## 2. Context（知识上下文 · 来自知识库的 Chunk）

以下是从知识库中检索到的多个 **独立知识 Chunk**。  
每一个 Chunk 都是一个**完整、可单独理解的知识单元**。

### [Chunk 1] 什么是 RAG

检索增强生成（Retrieval-Augmented Generation，RAG）  
是一种将外部知识检索与大语言模型生成相结合的技术范式，  
其核心思想是在生成回答前，先从可控知识库中检索相关信息，  
再将检索结果作为上下文输入给模型。

---

### [Chunk 2] 为什么需要 RAG

纯生成式模型存在幻觉、知识不可控与更新成本高的问题。  
RAG 通过“先查再答”的方式，引入显式知识来源，  
显著降低幻觉风险，并提升答案的可解释性与可维护性。

---

### [Chunk 3] RAG 的基本工作流程

一个最小可行的 RAG 工作流包括：  
Query 构造 → 文档检索 → 上下文拼接 → 模型生成回答。

---

### [Chunk 4] RAG 的工程价值

RAG 能降低幻觉风险、支持知识快速更新，  
并适合集成到企业系统与 Agent 架构中。

---

### [Chunk 5] RAG 的应用场景

RAG 常用于企业知识问答、客服系统、  
研究辅助生成以及 Agent 的知识底座。

---

### [Chunk 6] RAG 的挑战与注意事项

RAG 的效果依赖于检索质量、Chunk 设计、  
上下文长度控制以及配套的评价机制。

---

## 3. Objective（任务目标）

请基于以上知识 Chunk，完成以下任务：

1. 用 **结构清晰、信息准确** 的方式回答：
   - 什么是 RAG？
   - 为什么需要 RAG？
2. 简要说明 RAG 的工程价值与典型应用场景

---

## 4. Requirements（输出要求）

1. 使用 Markdown 输出  
2. 必须包含以下二级标题：
   - `## 什么是 RAG`
   - `## 为什么需要 RAG`
   - `## 工程价值与应用场景`
3. **不得引入 Context 中未出现的新概念**
4. 输出内容应可直接作为知识库说明文本复用

---

## 5. Evaluation（评价标准）

- 内容是否**完全来源于提供的 Chunk**
- 是否清晰区分不同问题的回答边界
- 是否适合被二次引用或系统调用

```

#### 4.3.4.3 步骤3：将LLM产生的反馈进行记录

`02-score-run.md`文件：

```markdown
## 什么是RAG

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成相结合的技术范式。其核心思想是在生成回答前，先从可控知识库中检索相关信息，再将检索结果作为上下文输入给模型。

其最小可行的工作流程包括：

- **Query 构造**：构建查询请求。
- **文档检索**：从知识库中检索相关文档。
- **上下文拼接**：将检索结果与输入组合。
- **模型生成回答**：由模型生成最终结果。

## 为什么需要RAG

纯生成式模型存在幻觉、知识不可控与更新成本高的问题。RAG 通过“先查再答”的方式，引入显式知识来源，能够：

- **显著降低幻觉风险**：通过参考真实文档生成内容。
- **提升可解释性与可维护性**：使答案的来源可追溯。
- **解决知识滞后**：规避模型原生知识更新成本高的问题。

## 工程价值与应用场景

### 工程价值

- **降低成本与风险**：降低幻觉风险，并支持知识的快速更新。
- **架构适配**：适合集成到企业系统与 Agent 架构中。
- **可优化性**：其效果可以通过优化检索质量、Chunk 设计、上下文长度控制以及配套的评价机制来持续提升。

### 典型应用场景

- **问答与客服**：常用于企业知识问答、客服系统。
- **研究辅助**：用于辅助生成研究内容。
- **Agent 支撑**：作为 Agent 的知识底座。
```

---

#### 4.3.4.4 步骤4：运行Critic/Refine

1. **编写`03-critic-prompt.md`**

```markdown
## 1. Setting（角色设定）

你是一个严格、保守的评估模块（Critic），  工作在一个需要稳定性、可验证性与可复用性的智能知识系统中。

你的职责不是改写内容，也不是补充新信息，  而是评估输出是否严格遵循给定的知识 Chunk 与交互协议。

---

## 2. Context（评估依据 · 知识 Chunk）

以下是系统允许模型使用的全部知识 Chunk。  你的评估必须完全基于这些内容，不得引入外部常识。

### [Chunk 1] 什么是 RAG

检索增强生成（Retrieval-Augmented Generation，RAG）  
是一种将外部知识检索与大语言模型生成相结合的技术范式，  
其核心思想是在生成回答前，先从可控知识库中检索相关信息，  
再将检索结果作为上下文输入给模型。

---

### [Chunk 2] 为什么需要 RAG

纯生成式模型存在幻觉、知识不可控与更新成本高的问题。  
RAG 通过“先查再答”的方式，引入显式知识来源，  
显著降低幻觉风险，并提升答案的可解释性与可维护性。

---

### [Chunk 3] RAG 的基本工作流程

一个最小可行的 RAG 工作流包括：  
Query 构造 → 文档检索 → 上下文拼接 → 模型生成回答。

---

### [Chunk 4] RAG 的工程价值

RAG 能降低幻觉风险、支持知识快速更新，  
并适合集成到企业系统与 Agent 架构中。

---

### [Chunk 5] RAG 的应用场景

RAG 常用于企业知识问答、客服系统、  
研究辅助生成以及 Agent 的知识底座。

---

### [Chunk 6] RAG 的挑战与注意事项

RAG 的效果依赖于检索质量、Chunk 设计、  
上下文长度控制以及配套的评价机制。

---

## 3. Input（待评估输出）

以下是 **Executor（基于 S.C.O.R.E 协议）生成的输出结果**：

<<<OUTPUT
（在此粘贴 01-score-prompt.md 生成的完整输出内容）
## 什么是 RAG

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成相结合的技术范式。其核心思想是在生成回答前，先从可控知识库中检索相关信息，再将检索结果作为上下文输入给模型。

其最小可行的工作流程包括：

- **Query 构造**：构建查询请求。
- **文档检索**：从知识库中检索相关文档。
- **上下文拼接**：将检索结果与输入组合。
- **模型生成回答**：由模型生成最终结果。

## 为什么需要 RAG

纯生成式模型存在幻觉、知识不可控与更新成本高的问题。RAG 通过“先查再答”的方式，引入显式知识来源，能够：

- **显著降低幻觉风险**：通过参考真实文档生成内容。
- **提升可解释性与可维护性**：使答案的来源可追溯。
- **解决知识滞后**：规避模型原生知识更新成本高的问题。

## 工程价值与应用场景

### 工程价值

- **降低成本与风险**：降低幻觉风险，并支持知识的快速更新。
- **架构适配**：适合集成到企业系统与 Agent 架构中。
- **可优化性**：其效果可以通过优化检索质量、Chunk 设计、上下文长度控制以及配套的评价机制来持续提升。

### 典型应用场景

- **问答与客服**：常用于企业知识问答、客服系统。
- **研究辅助**：用于辅助生成研究内容。
- **Agent 支撑**：作为 Agent 的知识底座。
OUTPUT

---

## 4. Evaluation Criteria（评价维度）

请从以下四个维度进行评估，每一项给出 **1–5 分** 的评分，并附带简要理由：

1. **Faithfulness（忠实性）**  
   - 输出内容是否完全来源于提供的 Chunk？
   - 是否存在臆造、扩展或引入新概念的情况？

2. **Completeness（完整性）**  
   - 是否覆盖了任务目标中要求回答的所有问题？
   - 是否遗漏关键 Chunk 所包含的重要信息？

3. **Boundary Control（边界控制）**  
   - 是否清晰区分不同问题的回答边界？
   - 是否出现内容串联、混合多个 Chunk 语义的问题？

4. **Reusability（可复用性）**  
   - 输出是否可直接作为知识库说明文本复用？
   - 是否结构清晰、语言稳定、无对话痕迹？

---

## 5. Output Format（裁判输出格式）

你的输出**必须且只能是一个 JSON 对象**，格式如下：

```json
{
  "scores": {
    "faithfulness": 0,
    "completeness": 0,
    "boundary_control": 0,
    "reusability": 0
  },
  "pass": true,
  "top_issues": [
    "问题 1（若有）",
    "问题 2（若有）"
  ],
  "fix_suggestions": [
    "可操作的修正建议 1",
    "可操作的修正建议 2"
  ]
}

```

2. **将LLM输出的反馈记录到`03-critic-run.json`**

```json
{
  "scores": {
    "faithfulness": 4,
    "completeness": 5,
    "boundary_control": 5,
    "reusability": 5
  },
  "pass": true,
  "top_issues": [
    "在“为什么需要 RAG”章节中引入了“解决知识滞后”这一表述，虽然语义逻辑与 Chunk 2 的“知识更新成本高”相符，但在词汇使用上超出了原 Chunk 定义范围。",
    "在“工程价值”章节中使用了“可优化性”作为小标题，原 Chunk 6 仅将其视为“挑战与注意事项”，并未显式定义为工程价值标题。"
  ],
  "fix_suggestions": [
    "将“解决知识滞后”修改为“解决模型知识更新成本高的问题”，以严格对齐 [Chunk 2] 的措辞。",
    "取消“可优化性”这一推导性标题，直接描述为“其效果依赖于检索质量、Chunk 设计、上下文长度控制及评价机制”，以保持对 [Chunk 6] 的原始表述忠实度。"
  ]
}
```

判定规则说明：

- 若 **Faithfulness < 4**，则 `pass = false`
- 若出现未在 Chunk 中出现的新概念，必须明确指出
- `fix_suggestions`必须是可以直接用于下一轮 Refine 的修改指令

3. **生成`04-refined-prompt.md`**

```markdown
## 1. Setting（角色设定）

你是一个**内容修正模块（Refiner）**，  
工作在一个需要**高一致性、低熵输出**的智能知识系统中。

你的职责不是重新创作内容，  
而是**严格依据裁判（Critic）的反馈，对已有输出进行最小必要修改**。

---

## 2. Context（允许使用的知识边界）

以下是系统允许你使用的**全部知识 Chunk**。  
你在修正过程中 **不得引入任何未在以下 Chunk 中出现的新概念或新信息**。

### [Chunk 1] 什么是 RAG
检索增强生成（Retrieval-Augmented Generation，RAG）  
是一种将外部知识检索与大语言模型生成相结合的技术范式，  
其核心思想是在生成回答前，先从可控知识库中检索相关信息，  
再将检索结果作为上下文输入给模型。

---

### [Chunk 2] 为什么需要 RAG
纯生成式模型存在幻觉、知识不可控与更新成本高的问题。  
RAG 通过“先查再答”的方式，引入显式知识来源，  
显著降低幻觉风险，并提升答案的可解释性与可维护性。

---

### [Chunk 3] RAG 的基本工作流程
一个最小可行的 RAG 工作流包括：  
Query 构造 → 文档检索 → 上下文拼接 → 模型生成回答。

---

### [Chunk 4] RAG 的工程价值
RAG 能降低幻觉风险、支持知识快速更新，  
并适合集成到企业系统与 Agent 架构中。

---

### [Chunk 5] RAG 的应用场景
RAG 常用于企业知识问答、客服系统、  
研究辅助生成以及 Agent 的知识底座。

---

### [Chunk 6] RAG 的挑战与注意事项
RAG 的效果依赖于检索质量、Chunk 设计、  
上下文长度控制以及配套的评价机制。

---

## 3. Input A（待修正的原始输出）

以下是上一轮 Executor 生成的输出内容：

<<<ORIGINAL_OUTPUT
（在此粘贴 01-score-prompt.md 的输出全文）
ORIGINAL_OUTPUT

---

## 4. Input B（Critic 的裁判反馈）

以下是 Critic 模块输出的 JSON 评估结果：

<<<CRITIC_FEEDBACK
（在此粘贴 03-critic-prompt.md 生成的 JSON）
CRITIC_FEEDBACK

---

## 5. Objective（修正目标）

请根据 Critic 的 `fix_suggestions` 与 `top_issues`：

1. **只修改必要的部分**，避免整体重写  
2. 消除所有被指出的越界、遗漏或结构问题  
3. 保证修正后输出：
   - 完全忠实于 Context 中的 Chunk
   - 满足原始 S.C.O.R.E 的全部 Requirements

---

## 6. Requirements（硬性要求）

1. **只输出修正后的最终内容**
2. 输出格式必须与原始输出保持一致（Markdown）
3. 不要解释修改过程
4. 不要输出修改说明或反思文本
5. 不要引用 Critic 的 JSON 内容

---

## 7. Completion Rule（完成判定）

当且仅当满足以下条件时，视为修正完成：

- 所有 Critic 指出的核心问题均被解决  
- 不再引入任何新的概念或表述风险  
- 输出内容可直接再次送入 Critic 进行复评

```

4. **记录LLM根据refine提示词生成的内容'

```markdown
## 什么是RAG

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成相结合的技术范式。其核心思想是在生成回答前，先从可控知识库中检索相关信息，再将检索结果作为上下文输入给模型。

其最小可行的工作流程包括：

- **Query 构造**：构造查询请求。
- **文档检索**：从知识库中检索相关文档。
- **上下文拼接**：将检索结果作为上下文输入给模型。
- **模型生成回答**：由模型生成回答。

## 为什么需要RAG

纯生成式模型存在幻觉、知识不可控与更新成本高的问题。RAG 通过“先查再答”的方式，引入显式知识来源，能够：

- **显著降低幻觉风险**：通过引入显式知识来源。
- **提升答案的可解释性与可维护性**：使知识来源可控。
- **解决知识更新成本高的问题**：支持知识快速更新，规避纯生成式模型的局限。

## 工程价值与应用场景

### 工程价值

- **支持知识快速更新**：能够降低幻觉风险，并支持知识快速更新。
- **适合集成到企业系统与 Agent 架构中**：具有良好的工程适配性。
- **效果依赖性说明**：RAG 的效果依赖于检索质量、Chunk 设计、上下文长度控制以及配套的评价机制。


### 典型应用场景

- **企业问答与客服系统**：常用于企业知识问答、客服系统。
- **研究辅助生成**：用于研究辅助生成场景。
- **Agent 知识底座**：作为 Agent 的知识底座。

```

---

###  4.3.5. 任务五：代理层模拟——人工运行 Agent 循环


> 📌 **理论对应：**讲义 4.4.2（规划-工具-反思模式） & 4.4.3（多代理编排）


在前四个任务中，你已经分别完成了：

1. **知识层**：将知识拆解为可独立使用的 Chunk
2. **数据层**：为知识添加可检索、可判断的元数据
3. **交互层**：通过 S.C.O.R.E 协议稳定调用知识
4. **评价层**：通过 Critic–Refine 建立修正闭环


但这些步骤仍然是**“单次调用视角”。 本任务的目标，是站在 Agent 的角度，理解并手动模拟一次完整的Agent 工作循环。本实验不要求编写 Agent 程序， 而是通过人工角色切换，理解 Agent 的运行逻辑与职责分工。

完成本任务后，你应当能够：

- 理解 Agent 系统中 **规划（Plan）—执行（Act）—反思（Reflect）** 的基本结构
- 明确 **Executor / Critic / Refiner** 在 Agent 循环中的角色定位
- 认识到Agent并不是“更聪明的模型”，而是被拆分、被约束的工作流程

在本实验中，你将“扮演”或“切换”以下角色：

|Agent 角色| 在本实验中的对应               |
| ------------ | ---------------------- |
|**Planner**| 人工判断：这一步要做什么           |
|**Executor**| `01-score-prompt.md`   |
|**Critic**| `03-critic-prompt.md`  |
|**Refiner**| `04-refined-prompt.md` |

> 📌 **关键认知**： Agent ≠ 一个 Prompt ，Agent = 一组有明确职责与顺序的 Prompt 协作

#### 4.3.5.1 步骤1：Plan（人工规划下一步行动）

**操作说明：**

阅读当前任务目标，例如：“生成一段可复用的 RAG 概念说明文本”

然后人工回答以下问题（写在实验记录中）：

- 当前目标是什么？
- 是否已有合格输出？
- 如果没有，下一步应该：

    - 生成？
    - 评估？
    - 修正？

Plan示例`06-agent-plan.md`

```markdown
# Agent Plan（规划记录）

## 当前任务目标
- 目标说明：生成一段可入库的RAG概念说明文本

## 当前状态判断
- 是否已有合格输出：否
- 已知风险：
  - 可能存在概念边界不清
  - 输出稳定性未知

## 行动决策
- 本轮需要执行：
  - Executor
  - Critic
  - Refiner

## 进入循环原因
- 需要通过 Critic 判断输出是否越界或遗漏

```


>📌 这一步不调用模型， 而是训练你站在 Agent 的“调度视角”思考。

#### 4.3.5.2 步骤2：Act（执行任务）

根据规划结果，执行对应操作：

- 若需要生成 → 使用 `01-score-prompt.md`
- 若需要评估 → 使用 `03-critic-prompt.md`
- 若需要修正 → 使用 `04-refined-prompt.md`

Act示例'07-agent-executor-output.md`

```markdown
# Executor Output（原始生成结果）

> 使用 Prompt：01-score-prompt.md  
> 执行时间：2025-xx-xx

---

## 什么是RAG
（模型生成内容）

## 为什么需要RAG
（模型生成内容）

## 工程价值与应用场景
（模型生成内容）

```

#### 4.3.5.3 步骤3：Reflect（反思与判断）

在完成一轮 Executor → Critic → Refiner 后，  请人工判断以下问题，并记录在 `08-agent-reflection.md` 中：

- 输出是否已通过 Critic？
- 是否仍存在边界不清、概念越界的问题？
- 是否需要再来一轮 Refine？


```markdown
# Agent 运行反思记录（Agent Reflection）

## 1. 本轮 Agent 循环概览

- 任务目标：  
  生成一段**可复用、可入库的 RAG 概念说明文本**

- 使用的 Prompt / 模块：
  - Executor：`01-score-prompt.md`
  - Critic：`03-critic-prompt.md`
  - Refiner：`04-refined-prompt.md`

- 本轮循环编号：Round 1

---

## 2. Planner 视角：为什么要启动这一轮？

在开始本轮循环前，我的判断是：

- 已有输出：❌ 没有合格输出  
- 问题判断：
  - 初始生成可能存在概念边界不清
  - 需要通过 Critic 明确是否存在越界或遗漏

👉 决策：  
**启动一轮完整的 Executor → Critic → Refiner 循环**

---

## 3. Critic 结果摘要（关键信息）

Critic 的 JSON 输出显示：

- Faithfulness：4 / 5  
- Completeness：3 / 5  
- Boundary Control：3 / 5  
- Reusability：4 / 5  
- pass：false  

主要问题包括：

1. “工程价值”与“应用场景”部分存在轻微语义混合  
2. 对 RAG 工作流程的描述略显简略，未完全覆盖 Chunk 3  

---

## 4. Refiner 执行情况

根据 Critic 给出的 `fix_suggestions`：

- 对“工程价值”与“应用场景”进行了拆分与重组
- 补充了对 RAG 工作流程的完整表述
- 未引入任何 Context 中未出现的新概念

Refiner 输出文件：

- `refiner-output-round1.md`

---

## 5. Reflect：是否需要进入下一轮？

### 当前判断

- 是否通过 Critic 的核心约束：✅ 是  
- 是否仍存在明显越界风险：❌ 否  
- 是否满足“可直接入库复用”：✅ 是  

### 决策结果

👉 **本轮 Agent 循环结束，不再进入下一轮**

---

## 6. 本轮 Agent 运行的关键收获

1. **Agent 的稳定性来自流程，而不是模型“更聪明”**
2. Critic 的价值在于：
   - 明确指出“哪里不合规”
   - 而不是要求“写得更好”
3. Refiner 的角色是：
   - 最小化修改
   - 而不是重新生成

---

## 7. 反思总结（一句话）

> 本实验让我理解到，  
> **Agent 并不是一次对话，而是一个可以被中断、评估和收敛的循环系统。**

```

>📌 若判断“需要继续”，则回到 **Plan**，开启下一轮循环。

---

## 5. 实验成果提交方式
### 5.1 统一提交根目录

所有实验成果请统一提交至：`08-Workspace/Assignment-M04/`，在提交根目录下，请按 **小组 → 个人** 两级目录组织成果：

```markdown
📁 08-Workspace/Assignment-M04/
├─ 📁 Group-A/
│  ├─ 📁 Alice/
│  │  │─ 01-score-prompt.md
│  │  │─ 02-score-run.md
│  │  │─ 03-critic-prompt.md
│  │  │─ 03-critic-run.json
│  │  │─ 04-refined-prompt.md
│  │  │─ 05-refined-run.md
│  │  │─ 06-agent-plan.md
│  │  │─ 07-agent-executor-output
│  │  └─ 08--agent-reflection
│  │─📁 Bob/
│  │     └─ （同上结构）
│─📁 Group-B/
│  └─📁 Charlie/
│     └─ （同上结构）
```
## 5.2 Pull Request 作业提交流程（正式提交）

当小组组员完提交后，需由 **组长** 提交最终 PR。
#### 5.2.1 步骤 1：Commit 规范

Commit message：

2. `git commit -m '[M04]`YouName`提交Lab04实验文件'`

#### 5.2.2 步骤 2：Push 至队长仓库

1. `git push origin main`

#### 5.2.3 步骤 3：Pull Request到主仓库

PR标题规范：

1. `GroupName`提交第四周章实验成果`

PR 内容须包含：

1. `- 文件路径`
2. `- 本次更新摘要`

#### 5.2.4 步骤4：等待讲师Review → Merge

讲师/助教会进行审核并给予意见。

🎉 恭喜完成 Lab04！

这意味着你已经从“写 Prompt”，迈入了工程化管理智能行为的阶段。

---
## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025 Gitconomy Research社区。
