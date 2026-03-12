# MCP 学习手册（Model Context Protocol）

MCP（Model Context Protocol）是一种开放协议标准，旨在让大型语言模型（LLM）与外部系统、数据源、工具、服务等实现规范化、安全的交互，从而使智能体系统能够突破单一模型训练语料的限制，获得实时相关的知识与操作能力。MCP 的出现是 AI 系统可扩展性与跨系统互操作性的重要里程碑。

本学习手册既包括了 MCP 的基础理论、协议架构与工作机制，又紧密结合 ModelScope MCP 在实操中的应用方式，是你在构建与实验 MCP 相关智能体系统时可以直接参考的入门与实战指南。

---

## 1. MCP 协议概述：是什么与为什么

### 1.1 MCP的定义

MCP 即 **Model Context Protocol**，是一种开放、标准化的协议，用于连接 LLM 与各种外部数据源与工具，使其能够在处理请求时获取或操作必要的信息与功能。该协议由 Anthropic 发起，并作为开源项目被广泛支持。 ([Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol?utm_source=chatgpt.com "Model Context Protocol"))

MCP 的核心目标是：

1. **扩展模型能力边界**：让智能体访问训练之外的实时信息
2. **标准化交互接口**：不再为每个系统建立特定适配器
3. **促进工具生态互联**：实现模型与系统间统一通信

作为协议，它通常定义了：

- **消息格式与传输协议（如 JSON-RPC）**
- **客户端（client）与服务器（server）交互规范**
- **上下文传递机制**
- **工具与数据源的能力抽象与调用方式**

MCP 类似于早期用于代码编辑器的 **Language Server Protocol（LSP）**，旨在通过标准化协议降低系统集成成本。

---

### **1.2 为什么需要 MCP 协议**

LLM 在面对实时任务时常常受限于其预训练语料。这就导致：

- 无法访问最新信息
- 无法直接操作系统与业务流程
- 对外部应用的交互能力弱

MCP 协议填补这一空白，通过本学习手册既包括了 MCP 的基础理论、协议架构与工作机制，又紧密结合 ModelScope MCP 在实操中的应用方式，是你在构建与实验 MCP 相关智能体系统时可以直接参考的入门与实战指南。标准化的方式让智能体获得实时上下文和操作能力，从而真正成为一个能“懂上下文、会行动”的系统。这极大地提升了 Agent 系统的实用性与规模化能力。

此外，MCP 协议支持双向交互，使得智能体能 请求外部数据/功能，并将处理结果返回模型，是构建复杂智能体系统的强力基础。

---

## 2. MCP 在 ModelScope 平台中的定位

[ModelScope](https://modelscope.cn/) 是一个提供模型探索、推理、训练、部署和应用的一站式服务平台。 在 ModelScope 平台上，MCP 被集成为生态的一部分，提供一个叫做 MCP 广场 的能力中心，用于：

- 聚合服务托管的 MCP Server
- 提供多种 MCP 工具
- 以标准协议让外部客户端（例如 Cherry Studio）接入并调用这些服务

用户可以在 ModelScope MCP 广场浏览、启用和管理多种 MCP 服务，这使得智能体能够轻松访问图片生成、搜索、记忆系统等能力

ModelScope 的MCP Server通常托管在该平台上，并提供包括：

|服务类型|示例|
|---|---|
|模型推理服务|文本/图像/视频生成|
|数据检索|文档索引与搜索|
|记忆接口|长期记忆访问|
|工具调用|外部 API 与系统操作|

MCP Server 运行时通常要求用户配置API Token，并通过MCP客户端连接。

---

## 3. MCP 核心机制与工作流程

### 3.1 MCP 架构组成

MCP 协议的典型架构分为三部分：

1. **MCP 客户端（Client）**
    运行在智能体中，将模型的请求转换为 MCP 标准格式

2. **MCP 服务器（Server）**
    对接实际能力（模型推理、数据库或工具 API），并根据协议返回结果

3. **上下文管理系统（Context Manager）**
    负责处理会话状态、权限和调用数据


这种架构使得不同客户端可以在不同语言和环境下与同一 MCP Server 交互，而 MCP Server 也可以标准化地对外暴露功能。

---

### **3.2 基本工作流程**

典型的 MCP 工作流程如下：

1. 智能体通过 MCP Client 将操作请求序列化成 MCP 协议格式。
2. MCP Client 与 MCP Server 建立连接（如 HTTP/WebSockets + JSON-RPC）。
3. MCP Server 接收请求，调用实际后端服务（如模型、数据库、API）。
4. MCP Server 以标准响应返回结果。
5. MCP Client 将结果重新映射给智能体模型或工作流。

这个流程的优点在于：

- **统一接口与格式**
- **跨系统扩展性**
- **易于组合多能力服务**

---

## 4. MCP 实践：接入与使用（以 ModelScope 为例）

### **4.1 获取 MCP 服务**

在 ModelScope MCP 广场（[https://modelscope.cn/mcp）中可以发现托管的](https://modelscope.cn/mcp%EF%BC%89%E4%B8%AD%E5%8F%AF%E4%BB%A5%E5%8F%91%E7%8E%B0%E6%89%98%E7%AE%A1%E7%9A%84) MCP Server。

使用 MCP 服务的一般步骤：

1. 注册 ModelScope 账号
2. 进入 MCP 广场并选择服务
3. 复制该服务的 API Token/连接信息
4. 在 MCP 客户端（如 Cherry Studio）中配置该服务

在 Cherry Studio 中，可以通过设置同步 ModelScope MCP Servers 并粘贴 API Token 来访问 ModelScope 广场上的所有 MCP 服务。 ([docs.cherry-ai.com](https://docs.cherry-ai.com/docs/en-us/advanced-basic/mcp/tian-jia-modelscope-mcp-fu-wu-qi?utm_source=chatgpt.com "Add ModelScope MCP Server"))

---

### **4.2 在智能体中调用 MCP 服务**

一旦配置完 MCP Server，智能体即可通过标准协议调用这些服务，例如：

- **语义检索与搜索**
- **访问数据库或知识库接口**

这种调用机制使得 Cherry Studio 或其它客户端能够扩展其工具集能力，而不必手工实现每个能力的适配。

---

## 5. MCP 的优势与生态价值

MCP 的出现有如下几方面的重要意义：

- **标准化工具接入**：避免针对每个工具建立接口适配
- **跨平台互操作性**：客户端可在不同环境复用 MCP Server
- **能力组合灵活度高**：智能体可以组合多个 MCP Server
- **生态规模效应**：大量服务在 MCP 广场汇聚，有利于生态增长

例如，MCP 广场中已有大 MCP Server 服务，覆盖模型推理、搜索、自动化等多种功能，为智能体构建复杂工作流提供天然支持。

---

## 6. MCP 与 RAG 的差异与互补

MCP 与传统 **RAG（检索增强生成）** 的主要区别在于：

|维度|RAG|MCP|
|---|---|---|
|作用对象|结构化语料检索|工具、系统、外部资源|
|动态性|静态知识|实时服务交互|
|依赖方式|向量匹配|协议调用|
|扩展性|有限|高|

简言之，MCP 的目标是让模型可以直接调用能力和资源，而 RAG 主要提供检索上下文。在复杂智能体系统中，两者可以互补。

---
## 7.  MCP 典型使用场景

MCP 的设计适用于许多场景：

- 智能化客服可以通过 MCP 访问业务系统，实现查询与下单
- 多模态创作系统可调用图像与视频生成服务
- 数据库查询代理（如 AI2SQL）根据自然语言生成查询
- 智能自动化工作流控制和执行跨系统操作

在 ModelScope 社区还有一些实战案例，如利用 MCP 实现自动化短视频创作管道等。

---

## 8. MCP 的前沿与发展趋势

随着业界对开放标准需求的增长，MCP 得到了主流 AI 平台的采纳。诸如 OpenAI、DeepMind、Microsoft 等平台已经开始支持或展示MCP 协议集成案例，而 ModelScope 则在中国生态进行了广泛推广。

---

## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025 Gitconomy Research社区。
