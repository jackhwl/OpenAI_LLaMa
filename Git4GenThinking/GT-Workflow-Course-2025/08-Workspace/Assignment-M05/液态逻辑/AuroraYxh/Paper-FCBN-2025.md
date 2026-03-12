---
uuid: paper-fcbn-2025
type: Paper
status:
  - Stable
venue: ICCV 2025
title: Function-centric Bayesian Network for Zero-Shot Object Goal Navigation
authors: Sixian Zhang, Xinhang Song, et al.
tags:
  - "#ZeroShotObjectNav"
  - "#BayesianNetwork"
  - "#LLM-Reasoning"
  - "#FunctionCentric"
related_questions:
  - FCBN 如何利用“功能”来解决长尾物体导航难题？
  - CounterfactCoT 提示词策略是如何构建贝叶斯网络的？
  - FCBN 的贝叶斯推理公式是如何更新目标概率的？
---

## 1. 核心创新：Function-centric (以功能为中心)
* **痛点**：传统的 LLM 方法通常将环境转译为文本描述（如“看到床”），然后问 LLM “床旁边可能有啥”。这忽略了物体的**功能属性**，且容易产生幻觉。
* **核心假设**：物体是为了“功能”而存在的。通过推理“功能”（如：休息、烹饪），可以建立更鲁棒的物体-场景关联。
    * *例子*：与其记忆“椅子在桌子旁”，不如记忆“椅子提供**坐（Sitting）**的功能” -> “坐通常发生在**用餐区（Dining）**”。

## 2. 算法模块 A：概率语义地图 (Probabilistic Semantic Map)
FCBN 首先构建一个开放词汇的语义地图，作为感知的地基：
* **视觉栈**：
    * **检测**：使用 **YOLOv7** (常见物体) + **Grounding-DINO** (开放词汇物体/场景)。
    * **分割**：使用 **Mobile SAM** 获取精确掩码。
* **地图更新**：将 2D 观测投影到 3D 点云，再降维成 2D 栅格地图。每个栅格存储该位置属于某物体/场景的**置信度分数**，并进行加权平均更新。

## 3. 算法模块 B：FBN 的增量构建 (The Brain)
这是该论文最核心的算法贡献。它不是预先建好的，而是**边走边建**。
* **节点 (Nodes)**：
    * $O$ (物体): 观测到的具体物体（如 Chair）。
    * $S$ (场景): 观测到的房间类型（如 Bedroom）。
    * $F$ (功能组): 隐变量，如 "Resting", "Cooking"。
* **边 (Edges) 与 LLM 推理**：
    * **[[Concept-CounterfactCoT]](反事实思维链)**：为了防止 LLM 瞎猜，作者设计了一种特殊的 Prompt。不仅问“A 是否导致 B？”，还问“如果没有 A，B 还会存在吗？”。通过对比事实 ($P(Y|do(X=1))$) 和反事实 ($P(Y|do(X=0))$) 的概率来确定边的权重。
    * **连接规则**：当新物体 $O_{new}$ 被发现时，仅在一定距离阈值内（如 1.5m）寻找附近的 $F$ 节点建立连接，保证计算复杂度是线性的。

## 4. 算法模块 C：贝叶斯导航策略
* **概率推理**：
    目标 $T$ 在功能组 $F_k$ 中的后验概率计算公式：
    $$P(G_{f_k} | T) \propto P(T|F_k) \cdot \sum ( P(F_k|S_i)P(S_i) + P(F_k|O_j)P(O_j) )$$
    这结合了**先验知识**（LLM 说目标常用于某种功能）和**观测证据**（我确实看到了支持该功能的场景/物体）。
* **路径规划**：
    * 生成概率热力图 (Probability Map)。
    * 选择概率最高的“前沿点 (Frontier)”或“已探索点”作为 Waypoint。
    * 使用 FMM (Fast Marching Method) 规划路径。