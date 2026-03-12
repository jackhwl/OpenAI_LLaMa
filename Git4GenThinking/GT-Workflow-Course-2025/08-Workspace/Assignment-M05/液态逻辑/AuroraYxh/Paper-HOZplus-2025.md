---
uuid: paper-hozplus-2025
type: Paper
status:
  - Stable
venue: IEEE TPAMI 2025
title: "HOZ++: Versatile Hierarchical Object-to-Zone Graph for Object Navigation"
authors: Sixian Zhang, Xinhang Song, et al.
tags:
  - "#GraphConstruction"
  - "#HierarchicalMemory"
  - "#SpatialClustering"
  - "#ZoneNavigation"
related_questions:
  - HOZ++ 如何定义 "Zone" (区域)？
  - 如何在线更新图结构以适应新环境？
  - 显式引导 (Explicit Guidance) 是如何生成子目标的？
---
## 1. 核心创新：Hierarchical Graph (分层图谱)
* **痛点**：扁平的语义地图容易让机器人“迷路”，因为它缺乏对整体布局的理解。
* **核心概念**：**[[Concept-Zone]]（区域）**。Zone 是介于 Object (太细) 和 Scene (太粗) 之间的中间层。
    * *定义*：Zone 是一组在空间上紧密聚集的物体集合（例如：沙发+茶几+地毯 = "休息区 Zone"）。

## 2. 算法模块 A：图的构建与融合 (Graph Construction)
HOZ++ 采用“离线学习 + 在线适应”的策略：
* **环境特定图 (Environment-Specific Graph)**：
    * **聚类 (Clustering)**：使用滑动窗口收集物体共现特征，用 **K-Means** 聚类生成 Zone 节点。
    * **命名**：利用 LLM 根据 Zone 里的物体给它起个名（如 Living Room Area）。
* **图融合 (Graph Merging)**：
    * 将多个训练环境的图通过 **Kuhn-Munkres 算法**（二部图最大权匹配）进行融合，生成一个通用的先验图 HOZ++ Graph。

## 3. 算法模块 B：在线更新机制 (Online Adaptation)
这是 TPAMI 版本相比 ICCV 版本的重大升级。
* **公式**：
    $$V(t) = \lambda Z_{cur} f_t^T + (1 - \lambda Z_{cur} Z_{cur}^T) V(t-1)$$
    * *含义*：当机器人在新环境看到一个 Zone 时，它会用当前的观测 $f_t$ (Bag-of-objects) 微调记忆中的通用 Zone 节点 $V(t)$。这使得 Agent 能适应“别人家的厨房”和“通用厨房”的差异。

## 4. 算法模块 C：显式引导导航 (Explicit Guidance)
这部分直接对应你想要的“地图导航”思路。
* **定位**：根据当前视野物体，在图中找到匹配的 `Current Zone Node`。
* **规划**：在图上搜索从 `Current Zone` 到 `Target Zone` 的最短路径。
* **子目标 (Sub-goal)**：路径上的**下一个 Zone** 被选为子目标。
* **执行**：在 2D 地图上计算该 Zone 的中心点，标为一个显式的 Waypoint，让机器人走过去。