# AWS Bedrock Integration Summary

## 概述

成功将 AWS Bedrock 支持集成到 HelloAgents 框架中。现在可以使用 Amazon Bedrock 服务（包括 Claude 3.5 Sonnet 等模型）作为 LLM 后端。

## 主要变更

### 1. 核心 LLM 模块更新 (`pkg/HelloAgents/hello_agents/core/llm.py`)

#### 新增功能:

1. **添加 Bedrock 提供商支持**
   - 在 `SUPPORTED_PROVIDERS` 中添加 `"bedrock"`
   - 支持自动检测 AWS Bedrock 配置

2. **Provider 自动检测增强**
   - 检测 `AWS_REGION` 和 `AWS_BEDROCK_ENABLED` 环境变量
   - 检测 `LLM_BASE_URL=bedrock` 配置
   - 智能判断是否使用 Bedrock

3. **凭证解析**
   - Bedrock 不需要 API key，使用 AWS credentials
   - 返回 AWS region 作为配置信息
   - 默认 region: `us-east-1`

4. **客户端初始化**
   - 使用 `boto3.client('bedrock-runtime')` 创建 Bedrock 客户端
   - 处理 boto3 未安装的情况
   - 验证 AWS credentials 配置

5. **消息格式转换**
   - `_convert_messages_to_bedrock_format()`: 将 OpenAI 格式转为 Bedrock 格式
   - 单独处理 system prompt
   - 支持 user 和 assistant 角色

6. **Bedrock API 调用**
   - `_call_bedrock_stream()`: 流式响应
   - `_call_bedrock()`: 非流式响应
   - 支持所有 Anthropic Claude 模型

7. **主要方法更新**
   - `think()`: 增加 Bedrock 流式调用分支
   - `invoke()`: 增加 Bedrock 非流式调用分支
   - `_get_default_model()`: 添加 Bedrock 默认模型

8. **默认模型**
   - Bedrock 默认: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`

### 2. 文档和示例

#### 新增文件:

1. **`BEDROCK_SETUP.md`** - 完整的 Bedrock 配置指南
   - AWS credentials 配置方法
   - 环境变量设置
   - 支持的模型列表
   - 区域选择建议
   - 成本考虑
   - 故障排查

2. **`example_bedrock.py`** - Bedrock 使用示例
   - 基础 LLM 调用
   - Agent 对话
   - 流式和非流式响应演示

3. **`test_bedrock_agent.py`** - 完整的测试脚本
   - 基础对话测试
   - 工具增强测试
   - 流式响应测试
   - 动态工具管理测试

4. **`env.template`** - 环境变量配置模板
   - 包含所有支持的 LLM 提供商配置示例
   - Bedrock 配置示例

#### 更新文件:

5. **`pkg/HelloAgents/README.md`**
   - 在支持的提供商表格中添加 AWS Bedrock
   - 添加 Bedrock 配置指南链接

## 技术实现细节

### Bedrock 消息格式

OpenAI 格式:
```python
[
    {"role": "system", "content": "你是一个助手"},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！"}
]
```

Bedrock 格式:
```python
{
    "system": "你是一个助手",  # 单独的系统提示
    "messages": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！"}
    ]
}
```

### 流式响应处理

Bedrock 流式响应事件格式:
```python
{
    'chunk': {
        'bytes': b'{"type":"content_block_delta","delta":{"text":"..."}}'
    }
}
```

需要:
1. 解析事件流
2. 提取 JSON chunk
3. 检查 chunk type
4. 获取增量文本

### API 调用

流式调用:
```python
response = bedrock_client.invoke_model_with_response_stream(
    modelId=model_id,
    body=json.dumps(request_body)
)
```

非流式调用:
```python
response = bedrock_client.invoke_model(
    modelId=model_id,
    body=json.dumps(request_body)
)
```

## 配置方法

### 方式 1: 环境变量 (.env 文件)

```bash
# 明确指定使用 Bedrock
LLM_BASE_URL=bedrock
AWS_REGION=us-east-1
LLM_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0

# AWS Credentials (如果未通过 aws configure 配置)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

### 方式 2: 代码中显式指定

```python
from hello_agents import HelloAgentsLLM

llm = HelloAgentsLLM(
    provider="bedrock",
    model="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
)
```

### 方式 3: 使用 AWS CLI 配置

```bash
aws configure
# 然后在 .env 中只需设置:
LLM_BASE_URL=bedrock
```

## 使用示例

### 基础使用

```python
from hello_agents import HelloAgentsLLM

# 创建 LLM 实例
llm = HelloAgentsLLM(provider="bedrock")

# 调用模型
messages = [
    {"role": "user", "content": "你好"}
]

# 流式响应
for chunk in llm.think(messages):
    print(chunk, end="", flush=True)

# 非流式响应
response = llm.invoke(messages)
print(response)
```

### 与 Agent 集成

```python
from hello_agents import HelloAgentsLLM
from my_simple_agent import MySimpleAgent

llm = HelloAgentsLLM(provider="bedrock")

agent = MySimpleAgent(
    name="助手",
    llm=llm,
    system_prompt="你是一个友好的AI助手"
)

response = agent.run("请介绍一下自己")
print(response)
```

## 支持的 Bedrock 模型

### Anthropic Claude 系列

- `us.anthropic.claude-3-5-sonnet-20241022-v2:0` (推荐, 最新)
- `us.anthropic.claude-3-opus-20240229-v1:0` (最强推理)
- `us.anthropic.claude-3-sonnet-20240229-v1:0`
- `us.anthropic.claude-3-haiku-20240307-v1:0` (最快, 最经济)

### 其他模型

理论上支持所有 Bedrock 提供的模型，但主要测试了 Claude 系列。

## 依赖

### 新增依赖

- `boto3` - AWS SDK for Python (可选，仅使用 Bedrock 时需要)

### 安装

```bash
# 如果要使用 Bedrock
pip install boto3

# 或者更新 requirements.txt
pip install -r requirements.txt
```

## 兼容性

- ✅ 完全兼容现有的 HelloAgents API
- ✅ 支持流式和非流式响应
- ✅ 支持 SimpleAgent, ReActAgent 等所有 Agent 类型
- ✅ 支持工具调用
- ✅ 支持对话历史
- ✅ 无需修改现有代码，只需更改 provider 配置

## 测试

### 运行测试

```bash
# 基础示例
python example_bedrock.py

# 完整测试
python test_bedrock_agent.py
```

### 前置条件

1. 安装 boto3
2. 配置 AWS credentials
3. 确保 AWS 账号有 Bedrock 访问权限
4. 在 Bedrock 控制台启用相应模型

## 已知限制

1. **模型可用性**: 不同 AWS 区域的可用模型不同
2. **成本**: Bedrock 按 token 使用量计费
3. **延迟**: 取决于 AWS 区域和网络条件
4. **权限**: 需要 IAM `bedrock:InvokeModel` 权限

## 未来改进方向

1. 支持更多 Bedrock 模型系列 (Titan, Llama 等)
2. 添加成本估算功能
3. 支持 Bedrock Agent 功能
4. 添加重试和错误处理优化
5. 支持流式响应的取消
6. 添加 token 使用统计

## 代码质量

- ✅ 无 linter 错误
- ✅ 遵循现有代码风格
- ✅ 完整的错误处理
- ✅ 详细的文档和注释
- ✅ 提供完整示例

## 参考资料

- [AWS Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
- [Anthropic Claude 文档](https://docs.anthropic.com/)
- [boto3 文档](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- HelloAgents 原有文档

## 贡献者

本次集成基于用户提供的 `my_llm.py` 和 `llm_client.py` 实现，将相同逻辑整合到 HelloAgents 框架核心。

## 总结

AWS Bedrock 集成成功完成，现在 HelloAgents 框架支持:

1. **11+ LLM 提供商**: OpenAI, Bedrock, DeepSeek, Qwen, ModelScope, Kimi, GLM, Ollama, vLLM 等
2. **统一接口**: 所有提供商使用相同的 API
3. **自动检测**: 智能识别配置并选择合适的提供商
4. **流式响应**: 所有提供商都支持流式输出
5. **完整文档**: 详细的配置指南和示例

用户现在可以无缝切换不同的 LLM 后端，包括 AWS Bedrock，而无需修改应用代码。


