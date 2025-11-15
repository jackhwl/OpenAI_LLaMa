# AWS Bedrock 配置指南

本指南介绍如何在 HelloAgents 框架中使用 AWS Bedrock 服务。

## 前置要求

1. **AWS 账号**: 需要有有效的 AWS 账号
2. **Bedrock 访问权限**: 确保你的账号已开通 Bedrock 服务
3. **boto3 库**: 安装 AWS SDK for Python

```bash
pip install boto3
```

## AWS Credentials 配置

### 方式 1: 使用 AWS CLI 配置 (推荐)

```bash
# 安装 AWS CLI
pip install awscli

# 配置 credentials
aws configure
```

按提示输入:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region name (例如: us-east-1)
- Default output format (可以留空或选择 json)

### 方式 2: 环境变量

在 `.env` 文件中添加:

```bash
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-1
```

### 方式 3: IAM Role (在 EC2/Lambda 上运行时)

如果在 AWS 环境中运行，可以直接使用 IAM Role，无需配置 credentials。

## HelloAgents Bedrock 配置

### 配置 1: 在 .env 文件中指定

```bash
# 方式 1: 明确指定 base_url 为 bedrock
LLM_BASE_URL=bedrock
AWS_REGION=us-east-1

# 方式 2: 使用环境变量标记
AWS_BEDROCK_ENABLED=true
AWS_REGION=us-east-1

# 可选: 指定模型 (如果不指定，将使用默认模型)
LLM_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0
```

### 配置 2: 在代码中显式指定

```python
from hello_agents import HelloAgentsLLM

# 方式 1: 指定 provider
llm = HelloAgentsLLM(
    provider="bedrock",
    model="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
)

# 方式 2: 通过 base_url 触发 Bedrock
llm = HelloAgentsLLM(
    base_url="bedrock",
    model="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
)
```

## 支持的 Bedrock 模型

### Anthropic Claude 模型 (推荐)

```python
# Claude 3.5 Sonnet (最新, 性能最佳)
model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

# Claude 3 Opus (最强推理能力)
model = "us.anthropic.claude-3-opus-20240229-v1:0"

# Claude 3 Sonnet
model = "us.anthropic.claude-3-sonnet-20240229-v1:0"

# Claude 3 Haiku (快速, 经济)
model = "us.anthropic.claude-3-haiku-20240307-v1:0"
```

### 其他模型

Bedrock 还支持 Amazon Titan, Meta Llama, Cohere 等模型，但本框架主要测试了 Claude 系列。

## 完整使用示例

```python
from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from my_simple_agent import MySimpleAgent

# 加载环境变量
load_dotenv()

# 创建 LLM 实例
llm = HelloAgentsLLM(
    provider="bedrock",
    model="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
)

# 创建 Agent
agent = MySimpleAgent(
    name="Bedrock助手",
    llm=llm,
    system_prompt="你是一个友好的AI助手。"
)

# 使用 Agent
response = agent.run("你好，请介绍一下自己")
print(response)
```

## 区域选择

不同区域的 Bedrock 可用模型可能不同，推荐区域:

- **us-east-1** (美国东部 - 弗吉尼亚): 最全的模型支持
- **us-west-2** (美国西部 - 俄勒冈): 良好的模型支持
- **ap-southeast-1** (新加坡): 亚太地区访问
- **eu-west-1** (爱尔兰): 欧洲访问

## 成本考虑

Bedrock 按使用量计费:
- **输入 tokens**: 每 1K tokens 约 $0.003 - $0.015 (视模型而定)
- **输出 tokens**: 每 1K tokens 约 $0.015 - $0.075 (视模型而定)

Claude 3 Haiku 最经济，Claude 3 Opus 最强大但成本最高。

## 故障排查

### 问题 1: "boto3 not found"

```bash
pip install boto3
```

### 问题 2: "Unable to locate credentials"

检查:
1. 运行 `aws configure` 配置 credentials
2. 或设置环境变量 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`

### 问题 3: "Access Denied" / "UnauthorizedException"

检查:
1. IAM 用户/角色是否有 `bedrock:InvokeModel` 权限
2. 在 Bedrock 控制台中是否启用了相应的模型
3. 区域是否支持 Bedrock 服务

### 问题 4: "Model not found"

- 确认模型 ID 正确
- 在 AWS Bedrock 控制台检查该区域是否支持该模型
- 确认已在 Bedrock 控制台中请求访问该模型

## 性能优化

1. **选择合适的区域**: 选择地理位置较近的区域以降低延迟
2. **使用合适的模型**: 根据任务复杂度选择模型
   - 简单任务: Claude 3 Haiku
   - 一般任务: Claude 3.5 Sonnet
   - 复杂推理: Claude 3 Opus
3. **流式响应**: 使用 `think()` 或 `stream_invoke()` 获得更好的用户体验

## 参考资源

- [AWS Bedrock 官方文档](https://docs.aws.amazon.com/bedrock/)
- [Bedrock 定价](https://aws.amazon.com/bedrock/pricing/)
- [Anthropic Claude 文档](https://docs.anthropic.com/)
- [boto3 文档](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 测试脚本

运行测试脚本验证配置:

```bash
python example_bedrock.py
```

如果配置正确，你应该看到成功的响应输出。

