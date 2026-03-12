---
uuid: concept-counterfactcot
type: Concept
domain: LLM-Reasoning
tags: ["#PromptEngineering", "#Causality"]
status: stable
---

## 定义 (Definition)
**CounterfactCoT (反事实思维链)** 是一种专门用于增强 LLM 因果推理能力的提示词策略。它不仅要求 LLM 评估“A 存在会导致 B”，还强制 LLM 思考“如果 A 不存在，B 是否还会存在”，通过对比事实与反事实的概率差来确定因果关系的强度。

## 上下文 (Context)
在 [[Paper-FCBN-2025]] 中，该策略被用于构建 **FBN (功能中心贝叶斯网络)** 的边。它能有效抑制 LLM 的幻觉，仅保留那些具有强因果依赖（如：床 -> 睡觉功能）的连接。

## 关联概念
- **输出产物**: Bayesian Network Edges
- **应用场景**: 在你的融合方案中，你将使用此策略来推断 [[Concept-Zone]] 的功能属性（例如：这个区域有桌子和电脑，如果没有电脑，它还是办公区吗？）。