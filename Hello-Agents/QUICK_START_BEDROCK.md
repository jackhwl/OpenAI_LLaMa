# Quick Start: AWS Bedrock with HelloAgents

## 🚀 5分钟快速上手

### 第一步: 安装依赖

```bash
# 安装 boto3
pip install boto3

# 确保 HelloAgents 已安装
cd pkg/HelloAgents
pip install -e .
```

### 第二步: 配置 AWS Credentials

**选择一种方式:**

#### 方式 A: 使用 AWS CLI (推荐)

```bash
pip install awscli
aws configure
```

输入你的:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (例如: `us-east-1`)

#### 方式 B: 设置环境变量

创建或编辑 `.env` 文件:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-1

# 指定使用 Bedrock
LLM_BASE_URL=bedrock

# 可选: 指定模型 (不指定则使用默认模型)
LLM_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0
```

### 第三步: 运行测试

#### 测试 1: 基础示例

```bash
python example_bedrock.py
```

这将运行:
- ✅ 基础 LLM 调用
- ✅ Agent 对话
- ✅ 流式和非流式响应

#### 测试 2: 完整 Agent 测试

```bash
python test_bedrock_agent.py
```

这将测试:
- ✅ 基础对话 Agent
- ✅ 工具增强 Agent (计算器)
- ✅ 流式响应
- ✅ 动态工具管理

### 第四步: 在你的代码中使用

#### 最简单的方式

```python
from hello_agents import HelloAgentsLLM

# 自动检测配置 (从 .env 读取)
llm = HelloAgentsLLM()

messages = [{"role": "user", "content": "你好"}]
for chunk in llm.think(messages):
    print(chunk, end="", flush=True)
```

#### 显式指定 Bedrock

```python
from hello_agents import HelloAgentsLLM

llm = HelloAgentsLLM(
    provider="bedrock",
    model="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
)

messages = [{"role": "user", "content": "你好"}]
response = llm.invoke(messages)
print(response)
```

#### 与 Agent 集成

```python
from hello_agents import HelloAgentsLLM
from my_simple_agent import MySimpleAgent

llm = HelloAgentsLLM(provider="bedrock")

agent = MySimpleAgent(
    name="Bedrock助手",
    llm=llm,
    system_prompt="你是一个友好的AI助手"
)

response = agent.run("什么是人工智能？")
print(response)
```

## 📋 配置检查清单

运行测试前，请确认:

- [ ] 已安装 `boto3`
- [ ] AWS credentials 已配置 (通过 `aws configure` 或环境变量)
- [ ] `.env` 文件中设置了 `LLM_BASE_URL=bedrock`
- [ ] AWS 账号有 Bedrock 访问权限
- [ ] 在 [Bedrock 控制台](https://console.aws.amazon.com/bedrock/) 中启用了 Claude 模型

## 🔧 故障排查

### 问题: "ModuleNotFoundError: No module named 'boto3'"

**解决方案:**
```bash
pip install boto3
```

### 问题: "Unable to locate credentials"

**解决方案:**
```bash
# 配置 AWS credentials
aws configure

# 或在 .env 中设置
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

### 问题: "AccessDeniedException"

**可能原因:**
1. IAM 用户/角色没有 `bedrock:InvokeModel` 权限
2. 未在 Bedrock 控制台启用模型
3. 区域不支持 Bedrock

**解决方案:**
1. 在 IAM 中添加权限策略:
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "bedrock:InvokeModel",
        "Resource": "*"
    }]
}
```

2. 访问 [Bedrock 控制台](https://console.aws.amazon.com/bedrock/)
3. 在 "Model access" 中请求访问 Claude 模型
4. 确认使用支持 Bedrock 的区域 (如 us-east-1)

### 问题: "Model not found"

**解决方案:**
- 检查模型 ID 是否正确
- 确认该区域支持该模型
- 使用默认模型: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`

## 💡 推荐的 AWS 区域

- **us-east-1** (美国东部): 最全的模型支持 ⭐️推荐
- **us-west-2** (美国西部): 良好支持
- **ap-southeast-1** (新加坡): 亚太地区
- **eu-west-1** (爱尔兰): 欧洲地区

## 💰 成本估算

Bedrock 按 token 使用量计费:

| 模型 | 输入 (per 1K tokens) | 输出 (per 1K tokens) |
|------|---------------------|---------------------|
| Claude 3 Haiku | ~$0.00025 | ~$0.00125 |
| Claude 3.5 Sonnet | ~$0.003 | ~$0.015 |
| Claude 3 Opus | ~$0.015 | ~$0.075 |

**示例:**
- 一次典型对话 (~500 tokens): $0.001 - $0.01
- 100次对话: $0.1 - $1.0

## 📚 更多资源

- **完整配置指南**: [BEDROCK_SETUP.md](BEDROCK_SETUP.md)
- **集成说明**: [BEDROCK_INTEGRATION_SUMMARY.md](BEDROCK_INTEGRATION_SUMMARY.md)
- **环境变量模板**: [env.template](env.template)
- **AWS Bedrock 文档**: https://docs.aws.amazon.com/bedrock/

## ✅ 验证安装

运行这个简单的脚本验证配置:

```python
# verify_bedrock.py
from hello_agents import HelloAgentsLLM

try:
    llm = HelloAgentsLLM(provider="bedrock")
    print(f"✅ Provider: {llm.provider}")
    print(f"✅ Model: {llm.model}")
    print(f"✅ Region: {llm.base_url}")
    
    # 测试调用
    messages = [{"role": "user", "content": "Say 'Hello from Bedrock!'"}]
    response = llm.invoke(messages)
    print(f"✅ Response: {response}")
    print("\n🎉 Bedrock 配置成功!")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    print("\n请检查:")
    print("1. boto3 是否已安装")
    print("2. AWS credentials 是否配置正确")
    print("3. 是否有 Bedrock 访问权限")
```

运行:
```bash
python verify_bedrock.py
```

如果看到 "🎉 Bedrock 配置成功!"，说明一切就绪！

## 🎯 下一步

现在你可以:
1. 在 `test_simple_agent.py` 中切换到 Bedrock
2. 将现有项目的 LLM 后端改为 Bedrock
3. 探索不同的 Claude 模型
4. 集成到你的应用中

祝使用愉快! 🚀


