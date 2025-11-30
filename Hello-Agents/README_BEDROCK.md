# AWS Bedrock Support for HelloAgents

## 🎉 Overview

AWS Bedrock support has been successfully integrated into the HelloAgents framework. You can now use Amazon Bedrock's Claude models (and other supported models) as your LLM backend with the same simple API.

## 📦 What's New

### Core Features Added

✅ **Full Bedrock Integration** - Native support for AWS Bedrock API  
✅ **Auto-Detection** - Automatically detects Bedrock configuration  
✅ **Streaming Support** - Both streaming and non-streaming responses  
✅ **Message Format Conversion** - Automatic OpenAI ↔ Bedrock format conversion  
✅ **Multiple Models** - Support for all Claude 3/3.5 models  
✅ **Complete Compatibility** - Works with all existing HelloAgents features  

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install boto3
```

### 2. Configure AWS

```bash
aws configure
```

Or set in `.env`:

```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
LLM_BASE_URL=bedrock
```

### 3. Test Installation

```bash
python verify_bedrock.py
```

### 4. Use in Code

```python
from hello_agents import HelloAgentsLLM

# That's it! Auto-detects from .env
llm = HelloAgentsLLM(provider="bedrock")

messages = [{"role": "user", "content": "Hello!"}]
for chunk in llm.think(messages):
    print(chunk, end="", flush=True)
```

## 📁 New Files

| File | Purpose |
|------|---------|
| `BEDROCK_SETUP.md` | Complete configuration guide |
| `BEDROCK_INTEGRATION_SUMMARY.md` | Technical implementation details |
| `QUICK_START_BEDROCK.md` | 5-minute quick start guide |
| `example_bedrock.py` | Basic usage examples |
| `test_bedrock_agent.py` | Comprehensive test suite |
| `verify_bedrock.py` | Configuration verification script |
| `env.template` | Environment variable template |
| `README_BEDROCK.md` | This file |

## 🔧 Modified Files

| File | Changes |
|------|---------|
| `pkg/HelloAgents/hello_agents/core/llm.py` | Added Bedrock provider support |
| `pkg/HelloAgents/README.md` | Updated supported providers table |

## 📖 Documentation

### For Users

- **Quick Start**: [QUICK_START_BEDROCK.md](QUICK_START_BEDROCK.md) - Get started in 5 minutes
- **Full Setup Guide**: [BEDROCK_SETUP.md](BEDROCK_SETUP.md) - Complete configuration instructions

### For Developers

- **Integration Summary**: [BEDROCK_INTEGRATION_SUMMARY.md](BEDROCK_INTEGRATION_SUMMARY.md) - Technical details
- **Environment Template**: [env.template](env.template) - All configuration options

## 🧪 Testing

### Quick Verification

```bash
python verify_bedrock.py
```

### Basic Examples

```bash
python example_bedrock.py
```

### Full Test Suite

```bash
python test_bedrock_agent.py
```

### Use with Existing Tests

```bash
# Just change your .env to use Bedrock
LLM_BASE_URL=bedrock

# Then run your existing tests
python test_simple_agent.py
```

## 💡 Usage Examples

### Simple LLM Call

```python
from hello_agents import HelloAgentsLLM

llm = HelloAgentsLLM(provider="bedrock")
messages = [{"role": "user", "content": "What is AI?"}]
response = llm.invoke(messages)
print(response)
```

### Streaming Response

```python
from hello_agents import HelloAgentsLLM

llm = HelloAgentsLLM(provider="bedrock")
messages = [{"role": "user", "content": "Tell me a story"}]

for chunk in llm.think(messages):
    print(chunk, end="", flush=True)
print()
```

### With Agent

```python
from hello_agents import HelloAgentsLLM
from my_simple_agent import MySimpleAgent

llm = HelloAgentsLLM(provider="bedrock")
agent = MySimpleAgent(
    name="Assistant",
    llm=llm,
    system_prompt="You are a helpful AI assistant."
)

response = agent.run("Hello, how are you?")
print(response)
```

### With Tools

```python
from hello_agents import HelloAgentsLLM, ToolRegistry
from hello_agents.tools import CalculatorTool
from my_simple_agent import MySimpleAgent

llm = HelloAgentsLLM(provider="bedrock")
registry = ToolRegistry()
registry.register_tool(CalculatorTool())

agent = MySimpleAgent(
    name="Math Assistant",
    llm=llm,
    system_prompt="You are a helpful math assistant.",
    tool_registry=registry,
    enable_tool_calling=True
)

response = agent.run("What is 15 * 23 + 100?")
print(response)
```

## 🌍 Supported Models

### Claude 3.5 (Latest)

```python
model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"  # Recommended
```

### Claude 3

```python
model = "us.anthropic.claude-3-opus-20240229-v1:0"     # Most capable
model = "us.anthropic.claude-3-sonnet-20240229-v1:0"   # Balanced
model = "us.anthropic.claude-3-haiku-20240307-v1:0"    # Fastest
```

## 🗺️ Recommended Regions

- **us-east-1** 🌟 Most complete model support
- **us-west-2** Good support
- **ap-southeast-1** Asia-Pacific
- **eu-west-1** Europe

## 💰 Pricing

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|------------------------|
| Claude 3 Haiku | ~$0.00025 | ~$0.00125 |
| Claude 3.5 Sonnet | ~$0.003 | ~$0.015 |
| Claude 3 Opus | ~$0.015 | ~$0.075 |

## 🔍 Troubleshooting

### Common Issues

#### "Module 'boto3' not found"

```bash
pip install boto3
```

#### "Unable to locate credentials"

```bash
aws configure
# Or set in .env:
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
```

#### "AccessDeniedException"

1. Check IAM permissions (need `bedrock:InvokeModel`)
2. Enable model access in [Bedrock Console](https://console.aws.amazon.com/bedrock/)
3. Verify region supports Bedrock

#### "Model not found"

- Use supported region (us-east-1 recommended)
- Verify model ID is correct
- Check model is enabled in Bedrock Console

## ✅ Feature Comparison

| Feature | OpenAI | Bedrock | Status |
|---------|--------|---------|--------|
| Streaming | ✅ | ✅ | ✅ |
| Non-streaming | ✅ | ✅ | ✅ |
| System prompts | ✅ | ✅ | ✅ |
| Temperature control | ✅ | ✅ | ✅ |
| Max tokens | ✅ | ✅ | ✅ |
| Tool calling | ✅ | ✅ | ✅ |
| Agent support | ✅ | ✅ | ✅ |
| Auto-detection | ✅ | ✅ | ✅ |

## 🔄 Migration Guide

### From OpenAI to Bedrock

**Before:**
```python
# .env
OPENAI_API_KEY=sk-...
LLM_MODEL_ID=gpt-3.5-turbo
```

**After:**
```python
# .env
LLM_BASE_URL=bedrock
AWS_REGION=us-east-1
LLM_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0
```

Your code stays the same! Just change the configuration.

## 🎯 Next Steps

1. ✅ Configure AWS credentials
2. ✅ Run `python verify_bedrock.py`
3. ✅ Try `python example_bedrock.py`
4. ✅ Test with your existing code
5. ✅ Deploy to production

## 📚 Additional Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Claude API Documentation](https://docs.anthropic.com/)
- [HelloAgents Documentation](pkg/HelloAgents/README.md)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 🤝 Support

If you encounter issues:

1. Check the troubleshooting section in [BEDROCK_SETUP.md](BEDROCK_SETUP.md)
2. Verify configuration with `verify_bedrock.py`
3. Review AWS Bedrock console for access and permissions
4. Check AWS CloudWatch logs for API errors

## 📝 Summary

AWS Bedrock is now fully integrated into HelloAgents:

✅ **Easy Setup** - Configure in minutes  
✅ **Same API** - No code changes needed  
✅ **Auto-Detection** - Smart provider selection  
✅ **Full Features** - Streaming, tools, agents  
✅ **Production Ready** - Error handling, documentation  
✅ **Well Tested** - Comprehensive test suite  

**Enjoy using Claude 3.5 with HelloAgents!** 🚀🤖

---

For detailed technical information, see [BEDROCK_INTEGRATION_SUMMARY.md](BEDROCK_INTEGRATION_SUMMARY.md)



