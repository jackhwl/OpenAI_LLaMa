# GraphRAG 拓扑推理记录

## 1. 复杂推理问题 (Complex Query)
**问题**：针对未知环境中的长尾物体导航，如何利用区域（Zone）的先验知识来弥补视觉检测的幻觉问题？
**分析**：这个问题涉及两个核心痛点：
1. "视觉检测幻觉" -> 需要 [[Paper-FCBN-2025]] 的贝叶斯推理解决。
2. "区域先验知识" -> 需要 [[Paper-HOZplus-2025]] 的分层图谱支持。

## 2. 知识检索路径 (Retrieval Path)
Agent 在知识库中的“跳跃”过程如下：

**Step 1: 定位核心概念**
- 入口节点：[[Concept-Zone]]
- *发现*：Zone 提供了物体共现的统计特征，但缺乏因果推理能力。
- *跳转关联*：查看 [[Paper-FCBN-2025]] 寻找增强推理的方法。

**Step 2: 跨节点推理**
- 节点：[[Paper-FCBN-2025]]
- *发现*：FCBN 提出了 [[Concept-CounterfactCoT]]，可以通过“反事实推理”判断物体与功能的强关联。
- *思考*：能不能把这个推理用到 Zone 上？

**Step 3: 形成合成结论**
- 路径终点：[[Paper-HOZplus-2025]]
- *结论*：将 FCBN 的推理结果（功能概率）注入到 HOZ++ 的 Zone 节点中。
- *最终路径*：`[[Concept-Zone]]` <--> `[[Paper-FCBN-2025]]` <--> `[[Concept-CounterfactCoT]]`

## 3. 图谱拓扑截图 (Graph Screenshot)
![[lab05-graph-export.png]]
*(注：请在 Obsidian 中打开 Graph View，筛选出 FCBN, HOZ, Zone, CounterfactCoT 这几个节点，截图并粘贴在这里)*