```mermaid
graph TD
    %% 定义节点样式
    classDef dataNode fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef processNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,rx:10,ry:10;
    classDef decisionNode fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rhombus;
    classDef finalNode fill:#d5f5e3,stroke:#2ecc71,stroke-width:3px;
    classDef artifactNode fill:#ffffff,stroke:#666,stroke-width:1px,stroke-dasharray: 5 5;

    %% --- 阶段 1: Input ---
    Input[📄 1. Input Node:<br/>原始科研数据 results.csv]:::dataNode --> Extract Process;

    %% --- 阶段 2: Extract ---
    subgraph Stage_Extract ["⚙️ 2. Extract Node (结构化生成)"]
        ExtractProcess(🤖 AI 抽取与结构化):::processNode
        PromptConstraints[Inject: 基础科研数据背景 +<br/>结构化 JSON 输出限制提示] -.-> ExtractProcess
    end

    ExtractProcess --> InitialJSON[📄 Initial JSON Draft<br/>(提取的初步结构化数据)]:::artifactNode;
    InitialJSON --> ValidateDecision;

    %% --- 阶段 3: Validate ---
    ValidateDecision{🛡️ 3. Validate Node:<br/>Schema/规则校验}:::decisionNode;
    ValidateDecision -- "❌ 校验失败 (格式错误)" --> RetryPath1[🔄 返回重新生成] --> ExtractProcess;
    ValidateDecision -- "✅ 校验通过 (如描述所示)" --> ValidatedJSON[📄 Validated JSON<br/>(格式正确的中间态)]:::dataNode;

    %% --- 阶段 4: Refine (Thinking Chain Loop) ---
    ValidatedJSON --> RefineProcess;

    subgraph Stage_Refine ["🧠 4. Refine Node (Critic-Refine 迭代优化)"]
        RefineProcess(🧐 AI Critic 批判性评估):::processNode
        ScorePrompt[Inject: SCORE Prompt 提示词<br/>(Faithfulness/Completeness等)] -.-> RefineProcess
        RefineProcess --> CriticOutput[📋 Critic Evaluation JSON<br/>(评分/Top Issues/Fix Suggestions)]:::dataNode
        
        CriticOutput --> QualityDecision{⚖️ 质量是否满足要求?};
        
        %% --- 迭代回路 (The Loop) ---
        QualityDecision -- "❌ 不满足 (存在 Top Issues)" --> FeedbackLoop(🔄 Feedback Loop:<br/>将发现的问题与当前结果交付 AI 再生成):::processNode
        FeedbackLoop --> ExtractProcess
    end

    %% --- 最终输出 ---
    QualityDecision -- "✅ 满足要求 (迭代完成)" --> FinalOutput[🚀 Final Delivery:<br/>最终高质量 JSON 输出]:::finalNode;

    %% 链接样式调整
    linkStyle 5,11 stroke:#d32f2f,stroke-width:2px,fill:none; % 失败/回路路径标红
    linkStyle 4,12 stroke:#2ecc71,stroke-width:2px,fill:none; % 成功路径标绿
```



