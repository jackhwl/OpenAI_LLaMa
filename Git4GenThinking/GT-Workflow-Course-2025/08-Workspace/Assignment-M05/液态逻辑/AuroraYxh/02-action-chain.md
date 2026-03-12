# Agent Action Chain: Map-guided Bayesian Zone Graph

## 1. Global Goal (全局目标)
**任务**：设计一套算法，将 [[Paper-FCBN-2025]] 的功能推理能力融合进 [[Paper-HOZplus-2025]] 的区域图谱结构中。
**输入**：[[Paper-FCBN-2025]], [[Paper-HOZplus-2025]], [[Concept-Zone]]

## 2. Chain Execution Log (执行日志)

### 🔄 Turn 1: 数据结构对齐
**Thought (思考)**:
FCBN 是基于像素（Pixel）的，而 HOZ++ 是基于节点（Node）的。要融合它们，我必须先弄清楚两者的数学定义差异。
**Action (行动)**:
检索并对比 [[Paper-FCBN-2025]] 中的 "Probabilistic Semantic Map" 和 [[Paper-HOZplus-2025]] 中的 "Zone Node Definition"。
**Observation (观察)**:
- FCBN: 使用 $M \in R^{(N+2) \times H \times W}$ 栅格地图，每个格子存概率。
- HOZ++: 使用 $G=(V, E)$ 图结构，节点 $v_i$ 存储物体共现特征向量。
**Reflection (反思)**:
直接叠加不可行。需要设计一个“投影函数”，将 FCBN 计算出的像素级概率聚合（Aggregation）到 HOZ 的 Zone 节点上。

### 🔄 Turn 2: 推理机制注入
**Thought (思考)**:
解决了数据结构，现在要解决推理逻辑。如何让 Zone 具备“反事实推理”能力？
**Action (行动)**:
查阅 [[Concept-CounterfactCoT]] 的提示词策略。
**Result (产出)**:
设计新 Prompt：不仅仅问 LLM “Zone 里有什么”，还要问 “如果 Zone 失去了 [核心物体]，它还是 [功能区] 吗？”。
**Reflection (反思)**:
这可以过滤掉 HOZ++ 中由 K-Means 产生的噪声节点（即那些只是空间凑在一起但没有实际功能的区域）。

### 🔄 Turn 3: 导航策略修正
**Thought (思考)**:
有了概率 Zone，导航策略怎么变？
**Action (行动)**:
修改 [[Paper-HOZplus-2025]] 的 "Explicit Guidance" 模块。
**Plan**:
1. Global: 在 HOZ 图上搜索 $P(Target|Zone)$ 最高的节点。
2. Local: 到达该 Zone 后，再切换回 FCBN 的局部探索。

## 3. System Update (系统更新)
- [x] 新增概念：[[Concept-Zone-Probability-Aggregation]] (区域概率聚合)
- [ ] 待办：需要查阅 FMM (Fast Marching Method) 的具体实现库。