#!/usr/bin/env python3
"""
AWS Bedrock 使用示例
演示如何使用 HelloAgents 框架调用 AWS Bedrock 服务
"""

from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from my_simple_agent import MySimpleAgent

# 加载环境变量
load_dotenv()

def test_bedrock_basic():
    """测试基础 Bedrock 调用"""
    print("=" * 60)
    print("测试 1: 基础 Bedrock LLM 调用")
    print("=" * 60)
    
    # 方式1: 显式指定provider
    llm = HelloAgentsLLM(
        provider="bedrock",
        model="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    )
    
    messages = [
        {"role": "system", "content": "你是一个友好的AI助手。"},
        {"role": "user", "content": "请用一句话介绍自己。"}
    ]
    
    print("\n流式响应:")
    response = ""
    for chunk in llm.think(messages):
        response += chunk
    
    print(f"\n\n完整响应: {response}")


def test_bedrock_agent():
    """测试 Bedrock Agent"""
    print("\n" + "=" * 60)
    print("测试 2: Bedrock Agent 对话")
    print("=" * 60)
    
    # 创建 Bedrock LLM
    llm = HelloAgentsLLM(provider="bedrock")
    
    # 创建 Agent
    agent = MySimpleAgent(
        name="Bedrock助手",
        llm=llm,
        system_prompt="你是一个专业的AI助手，擅长解答技术问题。请用简洁专业的方式回答。"
    )
    
    # 测试对话
    response = agent.run("什么是AWS Bedrock？")
    print(f"\n最终响应: {response}")


def test_bedrock_invoke():
    """测试非流式调用"""
    print("\n" + "=" * 60)
    print("测试 3: Bedrock 非流式调用")
    print("=" * 60)
    
    llm = HelloAgentsLLM(provider="bedrock")
    
    messages = [
        {"role": "user", "content": "请列举3个Python的优点，用一句话总结。"}
    ]
    
    response = llm.invoke(messages)
    print(f"\n响应: {response}")


if __name__ == "__main__":
    """
    运行前请确保:
    1. 已安装 boto3: pip install boto3
    2. 已配置 AWS credentials (通过 aws configure 或环境变量)
    3. 在 .env 文件中配置:
       LLM_BASE_URL=bedrock
       或
       AWS_REGION=us-east-1
       AWS_BEDROCK_ENABLED=true
    4. 确保你的 AWS 账号有 Bedrock 访问权限
    """
    
    try:
        # 运行测试
        test_bedrock_basic()
        test_bedrock_agent()
        test_bedrock_invoke()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请检查:")
        print("1. AWS credentials 是否配置正确")
        print("2. 是否安装了 boto3: pip install boto3")
        print("3. AWS 账号是否有 Bedrock 访问权限")
        print("4. 模型 ID 是否正确")


