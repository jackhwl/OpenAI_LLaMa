# 第三章实验手册指南：把“提示词”变成可执行的工作流语言

## 1. 实验目标与成果物

### 1.1 你将完成的能力闭环

1. **Express**：把高熵自然语言输出“坍缩”为低熵结构化数据（Markdown / JSON）。
2. **Evaluate**：建立可计算的评价信号（规则校验 + 可选 LLM Judge）。
3. **Iterate**：用 Critic-Refine / Reflexion 做多轮修正，提升稳定性。
4. **System**：把上述模块串成“提示链”，并在 Obsidian Canvas 上完成可视化编排（选做）。

### 1.2 需要提交的成果物

- `01_prompt_unstructured.md`：非结构化提示（baseline）
- `02_schema.json`：你的 JSON Schema（数据契约）
- `03_prompt_structured.md`：结构化提示（要求严格 JSON 输出）
- `04_samples/`：至少 5 条输入与对应输出（成功/失败都保留）
- `05_validator.py`：本地校验脚本（JSON Schema + Pydantic 二选一或都做）
- `06_judge_prompt.md`：LLM-as-a-Judge 的裁判提示（可选）
- `07_iterate_log.md`：迭代日志（每轮：问题→反馈→修正点→结果）
- `08_canvas.png` 或 `08_canvas.md`：Obsidian Canvas 截图/导出（选做）
- `REPORT.md`：实验报告（结构见第 7 节）

---

## 2. 实验场景：新闻信息抽取（从“读懂”到“可执行”）

你要把一段新闻文本，抽取为结构化对象，供下游系统直接使用——这正对应讲义里“结构化数据作为工作流血液”的核心论断。

### 输入（示例，可自行替换）

把下面文本保存为 `lab03/input/news_01.txt`：

> 【示例新闻】2024 年以来，多家国内科技企业加快在大模型领域的布局。阿里云近日宣布升级通义千问系列大模型，在代码生成、多轮对话和行业知识理解等方面进行了优化，并已在政务、金融和制造等场景中展开试点应用。百度方面也表示，其文心大模型正在持续迭代，并通过开放平台向企业和开发者提供 API 服务。行业分析认为，大模型能力的提升有助于推动人工智能在企业级场景中的规模化落地，但同时也对算力供给、数据质量以及模型安全提出了更高要求。部分专家指出，在应用快速扩张的背景下，如何控制成本、避免“幻觉”问题，并确保合规使用，将成为企业面临的主要挑战......

---

## 3. 任务一：Baseline（非结构化提示）——先看见“高熵”

### 第一步：直接提示

打开 `01_prompt_unstructured.md`

```text
请阅读以下新闻，提取关键信息，告诉我它讲了什么、涉及哪些公司、整体情绪如何，并给出你认为最重要的一条风险提示。
```


### 第二步：复制这段 Prompt，粘贴到你正在使用的 LLM 对话界面

- 通义千问（Qwen）
- DeepSeek
- ChatGPT
- Kimi
- ......

### 第三步：运行与记录

- 用同一条新闻跑 3 次（或让 3 位同学跑一次）
- 把输出粘到 `04_samples/unstructured_run_*.md`
- 记录典型问题：遗漏、格式混乱、冗余、难以被程序解析（这就是高熵输出的工程代价）

> 这一对比实验直接呼应讲义中的“非结构化 vs 结构化 Schema”对比表。

---

## 4. 任务二：定义数据契约（JSON Schema）——把“意图”硬化为结构

### 第一步：先定字段（遵循 Schema 设计原则）

按“原子性/类型约束/自描述性”来拆字段，避免一个 `summary` 装所有东西。

建议最小字段集（你也可以扩展）：

- `topic`：主题（string）
- `companies`：公司列表（string[]）
- `sentiment`：情绪枚举（Positive/Neutral/Negative）
- `key_points`：要点列表（string[]，>=3）
- `risk_alert`：风险提示（string，<=120）
- `source_language`：输入语言（zh/en）

### 第二步：写出 Schema（保存为 `02_schema.json`）

```json
{
  "type": "object",
  "required": ["topic", "companies", "sentiment", "key_points", "risk_alert", "source_language"],
  "properties": {
    "topic": { "type": "string", "minLength": 2, "maxLength": 60 },
    "companies": { "type": "array", "items": { "type": "string" }, "minItems": 1, "maxItems": 10 },
    "sentiment": { "type": "string", "enum": ["Positive", "Neutral", "Negative"] },
    "key_points": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 8 },
    "risk_alert": { "type": "string", "minLength": 4, "maxLength": 120 },
    "source_language": { "type": "string", "enum": ["zh", "en"] }
  },
  "additionalProperties": false
}
```

> 这里体现“Schema 是数据契约”，以及“JSON 是系统集成的通用语”。

---

## 5.任务三：结构化提示（Structured Prompt）——输出必须“可执行”

### C1. 使用定界符隔离指令区与数据区（防注入 + 降歧义）

讲义明确建议使用 `"""` / `###` / `---` 等定界符做隔离。

写入 `03_prompt_structured.md`：

```text
你是“信息抽取模块”。你的任务是把输入新闻转换为严格 JSON。

【硬性要求】
1) 你的输出必须是“唯一的、完整的JSON对象”，不要输出任何解释文字。
2) JSON 必须符合我提供的JSON Schema（字段必须齐全，不可多字段）。
3) companies 必须是数组；sentiment必须是枚举值之一。
4) key_points至少3条，每条尽量短。

【JSON Schema】
<<<SCHEMA
（把 02_schema.json 内容粘贴到这里）
SCHEMA

【输入新闻】
<<<INPUT
（把 news_01.txt 内容粘贴到这里）
INPUT
```

### 第二步：粘贴到你正在使用的 LLM 对话界面，运行 3 次并保存样本

输出保存为：

- `04_samples/structured_run_1.json`
- `04_samples/structured_run_2.json`
- `04_samples/structured_run_3.json`

---

## 6. 任务四：评价层（Evaluate）——把“好不好”变成误差信号

讲义强调：没有评价就没有闭环，评价要产生可用的“误差信号”。

### 第一步：确定性指标（必须做）：JSON Schema 校验

创建 `05_validator.py`（命令行带注释，便于教学投影）：

```python
# 05_validator.py
# 目的：用 JSON Schema 对模型输出做“确定性校验”，把“格式/字段/类型错误”自动暴露出来

import json
from jsonschema import Draft7Validator

def load_json(path: str) -> dict:
    # 读取 JSON 文件
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main() -> None:
    schema = load_json("02_schema.json")                 # 载入数据契约（Schema）
    output = load_json("04_samples/structured_run_1.json")  # 载入模型输出（可改成循环）

    validator = Draft7Validator(schema)                  # 创建校验器
    errors = sorted(validator.iter_errors(output), key=lambda e: e.path)

    if not errors:
        print("✅ Schema 校验通过：输出可被下游系统直接消费")
        return

    print("❌ Schema 校验失败：发现以下问题：")
    for err in errors:
        print(f"- {list(err.path)}: {err.message}")

if __name__ == "__main__":
    main()
```

运行：

```bash
# 安装依赖（如环境未安装）
pip install jsonschema

# 执行校验
python 05_validator.py
```

### 第二步：语义/认知质量（选做）：LLM-as-a-Judge

写入 `06_judge_prompt.md`：

```text
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

【新闻原文】
<<<INPUT ... INPUT
【模型输出】
<<<OUTPUT ... OUTPUT
```

---

## 7. 任务五：迭代层（Iterate）——Critic-Refine / Reflexion 让系统变稳

### 第一步： Critic-Refine（必须做一轮）

- **Critic**：用 任务四第二步 的裁判输出（或你人工写的 top_issues）

- **Refine**：把 `OUTPUT + fix_suggestions` 喂回模型，要求“只输出修正后的 JSON”

建议写入 `07_iterate_log.md` 的模板：

```md
## Round 1
- 输入：news_01.txt
- 输出：structured_run_1.json
- 校验：通过/失败（贴 validator 结果）
- Critic 发现的问题：
  1) ...
  2) ...
- Refine 修改点：
  1) ...
- 结果：structured_run_1_refined.json（再次校验：通过/失败）

## Round 2（可选）
...
```

### 第二步：Reflexion（选做）：让模型写“反思文本”

在 Refine 前先让模型输出一段“我为什么错、下次怎么避免”的短反思（然后再要求输出最终 JSON）。
提示示例：

```text
先输出一段不超过 80 字的反思，说明你上次输出违反了哪些 Schema 约束；
然后输出修正后的 JSON（不要输出任何额外文字）。
```

---

## 8. 任务六：系统层（System）——提示链 + Obsidian Canvas 可视化编排（选做）

讲义指出：Markdown/JSON 是工作流常用格式，Canvas 可把提示链拓扑“画出来”。

### F1. 画布节点建议（最小 4 节点）

1. **Input Node**：贴新闻原文
2. **Extract Node**：结构化提示（输出 JSON）
3. **Validate Node**：粘贴校验规则（或运行结果）
4. **Refine Node**：Critic-Refine 修正提示


导出 Canvas 截图为 `08_canvas.png`（或导出为 Markdown）。

---

# REPORT.md（实验报告要求）

建议固定结构（便于批改与复用）：

1. **实验目标与工作流总览**（用一张小流程图/列表）
2. **Baseline 现象**：非结构化输出的 2-3 个典型问题（贴片段）
3. **Schema 设计**：字段选择理由（对应原子性/类型约束/自描述性）
4. **结构化提示策略**：定界符、输出约束、为何这样写
5. **评价机制**：validator 结果 +（可选）Judge 评分
6. **迭代日志**：至少 1 轮 Critic-Refine（前后对比）
7. **结论**：你认为“提示词作为软协议”最关键的工程收益是什么？

---

## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025 Gitconomy Research社区。
