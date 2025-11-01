### Vicuna
* https://github.com/ggerganov/llama.cpp
* https://huggingface.co/eachadea/ggml-vicuna-13b-1.1/tree/main
* download ggml-vicuna-13b-4bit-rev1.bin to models
* make
* ./main -i --interactive-first -r "### Human:" --temp 0 -c 2048 -n -1 --ignore-eos --repeat_penalty 1.2 --instruct -m ./models/ggml-vicuna-13b-1.0-uncensored-q4_2.bin 

### Dalai_Alpaca
* cd alpaca
* npx dalai serve

### EleutherAI_pythia

## [Deep Learnong AI courses](https://github.com/jackhwl/OpenAI_LLaMa/tree/main/DeepLearningAI)
## Career Essentials in Generative AI by Microsoft and LinkedIn

## Hello-Agents
### 第一部分：智能体与语言模型基础
- 第一章 初识智能体
  - 1.1 什么是智能体？
    - [Hello Agent](https://github.com/datawhalechina/Hello-Agents)
    - 1.1.1 传统视角下的智能体
    - 1.1.2 大语言模型驱动的新范式
    - 1.1.3 智能体的类型
  - 1.2 智能体的构成与运行原理
    - 1.2.1 任务环境定义
    - 1.2.2 智能体的运行机制
    - 1.2.3 智能体的感知与行动
  - 1.3 动手体验：5 分钟实现第一个智能体
    - Thought-Action-Observation
    - 1.3.1 准备工作
    - 1.3.2 接入大语言模型
    - 1.3.3 执行行动循环
  - 1.4 智能体应用的协作模式
    - 1.4.1 作为开发者工具的智能体
    - 1.4.2 作为自主协作者的智能体
    - 1.4.3 Workflow和Agent的差异
- 第二章 智能体发展史
  - 2.1 基于符号与逻辑的早期智能体
    - 2.1.1 物理符号系统假说
    - 2.1.2 专家系统
    - 2.1.3 SHRDLU
    - 2.1.4 符号主义面临的根本性挑战
  - 2.2 构建基于规则的聊天机器人
    - 2.2.1 ELIZA 的设计思想
    - 2.2.2 模式匹配与文本替换
    - 2.2.3 核心逻辑的实现
  - 2.3 马文·明斯基的心智社会
    - 2.3.1 对单一整体智能模型的反思
    - 2.3.2 作为协作体的智能
    - 2.3.3 对多智能体系统的理论启发
  - 2.4 学习范式的演进与现代智能体
    - 2.4.1 从符号到联结
    - 2.4.2 基于强化学习的智能体
    - 2.4.3 基于大规模数据的预训练
    - 2.4.4 基于大语言模型的智能体
    - 2.4.5 智能体发展关键节点概览
    - 2.5 本章小结
- 第三章 大语言模型基础
  - 3.1 语言模型与 Transformer 架构
    - 3.1.1 从 N-gram 到 RNN, LSTM
    - 3.1.2 Transformer 架构解析
    - 3.1.3 Decoder-Only 架构
  - 3.2 与大语言模型交互
    - 3.2.1 提示工程
    - 3.2.2 文本分词
    - 3.2.3 调用开源大语言模型
    - 3.2.4 模型的选择
  - 3.3 大语言模型的缩放法则与局限性
  - 3.4 本章小结
### 第二部分：构建你的大语言模型智能体
- 第四章 智能体经典范式构建
    ```
    ReAct (Reasoning and Acting): 一种将“思考”和“行动”紧密结合的范式，让智能体边想边做，动态调整。
    Plan-and-Solve: 一种“三思而后行”的范式，智能体首先生成一个完整的行动计划，然后严格执行。
    Reflection: 一种赋予智能体“反思”能力的范式，通过自我批判和修正来优化结果。
    ```
  - 4.1 环境准备与基础工具定义
    - 4.1.1 安装依赖库
      - pip install openai python-dotenv
    - 4.1.2 配置 API 密钥
    - 4.1.3 封装基础 LLM 调用函数
    - 4.2 ReAct
      - 4.2.1 ReAct 的工作流程
      - 4.2.2 工具的定义与实现
      - 4.2.3 ReAct 智能体的编码实现
      - 4.2.4 ReAct 的特点、局限性与调试技巧