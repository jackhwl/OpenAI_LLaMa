## 实验目标与工作流总览（用一张小流程图/列表）
unstructured_prompt->output1(baseline)  
schema_design INPUT structured_prompt  
structured_prompt->output(COMPARE_TO output1)
judge_prompt+output->ITERATE output
## Baseline 现象：非结构化输出的 2-3 个典型问题（贴片段）
1. 当非结构化prompt时,会出现相应的字段很不规范,层级不统一
```
**主要内容**：
...
**涉及公司**：
...
**整体情绪**：
...
### 最重要的风险提示
...
```

2. 对字段`整体情绪`判断过于中性,并没有什么可执行的意义
```
较为积极，主要关注大模型技术进展和应用，但也提到相关的挑战和风险。
```
```
新闻既肯定了大模型对人工智能在企业级场景落地的推动作用，也明确指出了当前面临的算力、数据、安全、成本等多重挑战，语气偏向客观理性。
```
```
- 积极：大模型的快速发展和技术优化带来了新的机遇，特别是在企业级应用领域。
- 谨慎：面对大模型应用的扩展，业内专家提醒注意控制成本、避免“幻觉”问题和确保合规使用。
```

## Schema 设计：字段选择理由（对应原子性/类型约束/自描述性）
字段设计"field":"constraints"  

字段原子性可以将复杂问题拆分最小单元,有[topic,companies,sentiment,key_points,risk_alert,source_language]  

约束类型可以明确字段类型,为后续核验提供标准  

自描述性可以辅助模型理解进行语义分割与分类

## 结构化提示策略：定界符、输出约束、为何这样写
使用`【】`作为定界符,将指令与内容部分分开,便于模型判断并执行  
输出约束 提醒强化模型输出规范,为辅助后续schema核验

## 评价机制：validator 结果 +（可选）Judge 评分
```
(LHY) ww@pc-SYS-4029GP-TRT:~/wwtest$ /home/ww/.conda/envs/LHY/bin/python /home/ww/wwtest/05_validator.py
✅ Schema 校验通过：输出可被下游系统直接消费
```
```
judge_output:
{
  "faithfulness": 5,
  "completeness": 4,
  "usefulness": 4,
  "top_3_issues": [
    "key_points 遗漏关键背景信息",
    "risk_alert 未关联具体要求与潜在影响",
    "sentiment 评价维度单一，未能反映复杂现状"
  ],
  "fix_suggestions": [
    "在 key_points 中补充优化重点（代码生成/多轮对话/行业知识）与试点领域（政务/金融/制造）",
    "为 risk_alert 增加具体挑战说明（如算力供给、数据质量、模型安全要求提升）",
    "将 sentiment 改为 'Cautiously Optimistic' 或补充说明积极趋势与挑战并存"
  ]
}
```
## 迭代日志：至少 1 轮 Critic-Refine（前后对比）

## Round 1
- 输入：news_01.txt
- 输出：structured_run_1.json
- 校验：通过/失败（贴 validator 结果）
```
(LHY) ww@pc-SYS-4029GP-TRT:~/wwtest$ /home/ww/.conda/envs/LHY/bin/python /home/ww/wwtest/05_validator.py
✅ Schema 校验通过：输出可被下游系统直接消费
```
- Critic 发现的问题：
  1) key_points 遗漏关键背景信息
  2) risk_alert 未关联具体要求与潜在影响
  3) sentiment 评价维度单一，未能反映复杂现状
- Refine 修改点：
  1) 在 key_points 中补充优化重点（代码生成/多轮对话/行业知识）与试点领域（政务/金融/制造）
  2) 为 risk_alert 增加具体挑战说明（如算力供给、数据质量、模型安全要求提升）
  3) 将 sentiment 改为 'Cautiously Optimistic' 或补充说明积极趋势与挑战并存

- 结果：structured_run_1_refined.json（再次校验：通过/失败）
```
(LHY) ww@pc-SYS-4029GP-TRT:~/wwtest/mcp$ /home/ww/.conda/envs/LHY/bin/python /home/ww/wwtest/mcp/05_validator.py
❌ Schema 校验失败：发现以下问题：
- ['sentiment']: 'Cautiously Optimistic' is not one of ['Positive', 'Neutral', 'Negative']
```

## Round 2
- 输入：OUTPUT + ['sentiment']: 'Cautiously Optimistic' is not one of ['Positive', 'Neutral', 'Negative']
- 输出：structured_run_1_refined.json
- 校验：通过/失败（贴 validator 结果）
```
(LHY) ww@pc-SYS-4029GP-TRT:~/wwtest/mcp$ /home/ww/.conda/envs/LHY/bin/python /home/ww/wwtest/mcp/05_validator.py
✅ Schema 校验通过：输出可被下游系统直接消费
```


## 结论：你认为“提示词作为软协议”最关键的工程收益是什么？

使用结构化提示词减少自然语言的熵值,使得输出结果更加可信可靠.虽然软协议可以要求模型输出规定格式,但是还是会出现无法满足硬系统的情况,需要使用外部验证判断.