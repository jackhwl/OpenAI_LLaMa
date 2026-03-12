### 问题
RAG在Agent系统中为什么重要？
### Graph推理路径
RAG → Agent → Action Chain
### 推理结论
RAG为Agent提供了可追溯、可更新的外部知识基础，
使其决策不再依赖模型的内隐记忆

### 对比反思
- 普通RAG：一次检索，只回答一个问题
- GraphRAG：沿知识关系组合多个Chunk，支持复合推理
在本实验中，我通过显式链接模拟了 Agent 的路径选择过程。