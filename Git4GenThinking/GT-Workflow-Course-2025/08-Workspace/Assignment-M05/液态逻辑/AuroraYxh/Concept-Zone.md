---
uuid: concept-zone
type: Concept
domain: Object-Navigation
tags:
  - "#SpatialRepresentation"
  - "#HOZ"
status:
  - Stable
---

## 定义 (Definition)
**Zone (区域)** 是一种介于底层物体 (Object) 和顶层场景 (Scene) 之间的中间层空间语义单元。它由一组在空间上紧密相邻且语义相关的物体集合构成（例如：沙发 + 茶几 + 地毯 = "休息区 Zone"）。

## 上下文 (Context)
在 [[Paper-HOZplus-2025]] 中，Zone 被用作导航的**子目标 (Sub-goal)**。相比于难以直接定位的小物体（如杯子），Zone 具有更大的空间范围和更稳定的语义特征，能有效减少机器人在未知环境中的搜索盲目性。

## 关联概念
- **上级概念**: [[Concept-Semantic-Map]] (语义地图)
- **应用场景**: 你的融合方案打算将 [[Paper-FCBN-2025]] 的贝叶斯概率计算附着在 Zone 节点上，而非像素点上。