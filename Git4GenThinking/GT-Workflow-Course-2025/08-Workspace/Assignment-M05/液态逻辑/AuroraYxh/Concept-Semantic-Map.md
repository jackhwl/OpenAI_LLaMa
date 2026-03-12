---
uuid: concept-semantic-map
type: Concept
domain: SLAM
tags: ["#Mapping", "#Perception"]
status: stable
---

## 定义 (Definition)
**Semantic Map (语义地图)** 是一种在几何地图（如栅格地图或点云）的基础上，叠加了环境语义信息（如物体类别、房间类型、功能标签）的空间表示形式。它使机器人不仅知道“哪里有障碍”，还知道“哪里是什么”。

## 上下文 (Context)
- 在 [[Paper-FCBN-2025]] 中，它是**概率性**的，存储物体存在的置信度。
- 在 [[Paper-HOZplus-2025]] 中，它是**分层**的，被划分为不同的 Zone。

## 关联概念
- **组成元素**: [[Concept-Zone]]