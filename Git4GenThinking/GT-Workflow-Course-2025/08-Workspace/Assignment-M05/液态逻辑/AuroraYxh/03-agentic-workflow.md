# Agentic Workflow: 科研算法融合助手

## 1. Workflow Definition (流程定义)

### Trigger (触发器)
**场景**：当发现两个不同算法（A 和 B）各有优劣，试图将它们结合时。
**输入**：两篇核心论文笔记 + 一个融合目标。

### Step 1: Retrieve (检索)
- **动作**：扫描论文笔记的 `Atomic Concepts` 和 `Algorithm Modules`。
- **关注点**：寻找 Common Ground（共同点，如都用了语义地图）和 Conflict Point（冲突点，如数据结构不同）。
- **工具**：Obsidian Search / Graph View。

### Step 2: Reason (推理/对齐)
- **动作**：分析 A 的输出能否作为 B 的输入？或者 A 的结构能否承载 B 的计算？
- **关键**：识别维度差异（Pixel vs Node, 2D vs 3D）。

### Step 3: Act (方案生成)
- **动作**：输出“融合架构图”或“伪代码”。
- **产出**：在 `10-Projects` 中创建新的 `Idea Note`。

### Step 4: Reflect (反思与循环)
- **动作**：自我质问“这个融合增加了计算量吗？收益值得吗？”。
- **输出**：若发现逻辑漏洞，返回 Step 1 补充检索遗漏的概念。

---

## 2. Workflow Validation (复用性验证)

**测试问题**：如何将 "Reinforcement Learning (RL)" 引入当前的 "Bayesian HOZ" 框架以提升动态避障能力？

**执行记录**：
1. **Retrieve**: 检索 [[Paper-HOZplus-2025]] (含导航策略) 和 RL 相关概念。
2. **Reason**: HOZ 目前是基于规则的 (FMM)，RL 是基于策略网络的。冲突点在于路径规划的控制权。
3. **Act**: 提出方案 —— 用 HOZ 做上层规划（给子目标），用 RL 做底层控制（局部避障）。
4. **Reflect**: 可行，但需要定义清晰的接口（Sub-goal 格式）。

**结论**：该工作流通过验证，具备科研复用性。