```json
你是严格、公正的评估员。请对“模型输出 JSON”进行评分并给出可操作的修正建议。
评分维度（1-5）：
1) Faithfulness：是否忠实于新闻事实（避免臆造）
2) Completeness：字段是否信息充分（尤其 key_points 与 risk_alert）
3) Usefulness：是否便于下游执行（字段值是否具体、可用）
输出也必须为 JSON：
{
  "faithfulness": int,
  "completeness": int,
  "usefulness": int,
  "top_3_issues": [string],
  "fix_suggestions": [string]
}
阅读文件 result.csv
<<<INPUT ... INPUT
{
    "meta_info": {
        "category": "研究进展汇报",
        "sentiment": "neutral",
        "tags": [
            "研究生",
            "图像识别",
            "实验分析",
            "中期汇报",
            "研究进展"
        ]
    },
    "core_event": "研究生在研究中期完成图像识别实验分析及result.csv数据获取，需向导师汇报本周工作总结、主要成果、问题分析及下周计划，确保总结全面准确。",
    "entities": {
        "people": [
            {
                "name": "研究生",
                "title": "研究人员",
                "stance": "完成图像识别实验分析，需全面准确汇报中期研究进展"
            },
            {
                "name": "导师",
                "title": "指导教师",
                "stance": "接收研究生的研究进展汇报，了解实验情况与后续计划"
            }
        ],
        "organizations": [
            "科研团队",
            "高校研究实验室"
        ]
    },
    "event_details": {
        "time": "研究中期（本周）",
        "location": "科研实验室/线上汇报场景",
        "key_data": [
            {
                "value": "99个epoch",
                "indicator": "模型训练迭代次数",
                "trend": "逐步迭代完成"
            },
            {
                "value": "1份",
                "indicator": "研究数据文件（result.csv）",
                "trend": "已获取"
            },
            {
                "value": "4个模块",
                "indicator": "汇报核心内容（工作总结、成果展示、问题分析、下周计划）",
                "trend": "需完整呈现"
            }
        ]
    },
    "analysis": {
        "background": "当前处于图像识别研究项目中期阶段，研究生需定期向导师同步研究进展，本周核心完成实验分析与数据收集工作，为确保导师全面掌握项目推进情况、及时指导后续研究，需按规范格式完成汇报。",
        "impact": "准确全面的汇报可帮助导师发现实验中潜在问题，为后续模型优化、研究方向调整提供指导；清晰的计划可保障项目按进度推进，助力顺利完成中期研究目标。",
        "quotes": [
            "需确保工作总结的全面性和准确性",
            "重点汇报图像识别实验分析成果及result.csv数据相关情况",
            "明确研究中期遇到的问题及针对性解决方案"
        ]
    }
}
<<<OUTPUT ... OUTPUT
```



```json
{
  "faithfulness": 4,
  "completeness": 3,
  "usefulness": 3,
  "top_3_issues": [
    "key_points 字段缺失，未明确列出关键要点",
    "risk_alert 字段缺失，未提及潜在风险及应对措施",
    "部分字段描述较为模糊，缺乏具体细节"
  ],
  "fix_suggestions": [
    "增加 key_points 字段，列出研究进展的关键要点，如实验方法、主要发现等",
    "增加 risk_alert 字段，指出可能的风险点及相应的预防或应对措施，如数据质量问题、技术瓶颈等",
    "细化 event_details 中的内容，提供更具体的数据和信息，例如实验的具体参数设置、结果的具体数值等"
  ]
}

```

