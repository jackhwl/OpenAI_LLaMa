# test_bedrock_agent.py
"""
测试 AWS Bedrock 集成的脚本
展示如何在 HelloAgents 框架中使用 AWS Bedrock

使用前请确保:
1. 安装 boto3: pip install boto3
2. 配置 AWS credentials (通过 aws configure 或环境变量)
3. 在 .env 中设置 Bedrock 配置 (参考 BEDROCK_SETUP.md)
"""

from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM, ToolRegistry
from hello_agents.tools import CalculatorTool
from my_simple_agent import MySimpleAgent

# 加载环境变量
load_dotenv()

# 创建 Bedrock LLM 实例
print("初始化 AWS Bedrock LLM...")
llm = HelloAgentsLLM(
    provider="bedrock",
    # 可选: 显式指定模型，不指定则使用默认模型
    # model="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
)

# 测试1:基础对话Agent（无工具）
print("\n" + "=" * 60)
print("=== 测试1: 基础对话 (AWS Bedrock) ===")
print("=" * 60)
basic_agent = MySimpleAgent(
    name="Bedrock基础助手",
    llm=llm,
    system_prompt="你是一个友好的AI助手，请用简洁明了的方式回答问题。"
)

response1 = basic_agent.run("你好，请介绍一下自己，并说明你运行在什么平台上")
print(f"\n基础对话响应: {response1}\n")

# 测试2:带工具的Agent
print("\n" + "=" * 60)
print("=== 测试2: 工具增强对话 (AWS Bedrock) ===")
print("=" * 60)
tool_registry = ToolRegistry()
calculator = CalculatorTool()
tool_registry.register_tool(calculator)

enhanced_agent = MySimpleAgent(
    name="Bedrock增强助手",
    llm=llm,
    system_prompt="你是一个智能助手，可以使用工具来帮助用户。运行在 AWS Bedrock 平台。",
    tool_registry=tool_registry,
    enable_tool_calling=True
)

response2 = enhanced_agent.run("请帮我计算 25 * 16 + 128")
print(f"\n工具增强响应: {response2}\n")

# 测试3:流式响应
print("\n" + "=" * 60)
print("=== 测试3: 流式响应 (AWS Bedrock) ===")
print("=" * 60)
print("流式响应: ", end="")
for chunk in basic_agent.stream_run("请用3点简要说明 AWS Bedrock 的优势"):
    pass  # 内容已在stream_run中实时打印

# 测试4:动态添加工具
print("\n" + "=" * 60)
print("=== 测试4: 动态工具管理 ===")
print("=" * 60)
print(f"添加工具前: {basic_agent.has_tools()}")
basic_agent.add_tool(calculator)
print(f"添加工具后: {basic_agent.has_tools()}")
print(f"可用工具: {basic_agent.list_tools()}")

# 查看对话历史
print(f"\n对话历史: {len(basic_agent.get_history())} 条消息")

# 测试5: 比较响应
print("\n" + "=" * 60)
print("=== 测试5: 技术问题测试 ===")
print("=" * 60)
response5 = basic_agent.run("什么是 Agent？用一句话解释")
print(f"\n响应: {response5}")

print("\n" + "=" * 60)
print("✅ 所有 Bedrock 测试完成!")
print("=" * 60)




