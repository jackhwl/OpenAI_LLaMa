#!/usr/bin/env python3
"""
Bedrock 配置验证脚本
快速验证 AWS Bedrock 是否配置正确
"""

from hello_agents import HelloAgentsLLM

def main():
    print("=" * 60)
    print("AWS Bedrock 配置验证")
    print("=" * 60)
    
    try:
        print("\n1️⃣ 创建 Bedrock LLM 实例...")
        llm = HelloAgentsLLM(provider="bedrock")
        
        print(f"   ✅ Provider: {llm.provider}")
        print(f"   ✅ Model: {llm.model}")
        print(f"   ✅ Region: {llm.base_url}")
        
        print("\n2️⃣ 测试 API 调用...")
        messages = [{"role": "user", "content": "Say 'Hello from Bedrock!' in one sentence."}]
        response = llm.invoke(messages)
        
        print(f"   ✅ 响应收到: {response[:100]}...")
        
        print("\n3️⃣ 测试流式响应...")
        print("   响应内容: ", end="")
        messages = [{"role": "user", "content": "Count from 1 to 3."}]
        full_response = ""
        for chunk in llm.think(messages):
            full_response += chunk
        
        print(f"\n   ✅ 流式响应成功，长度: {len(full_response)} 字符")
        
        print("\n" + "=" * 60)
        print("🎉 恭喜! AWS Bedrock 配置成功!")
        print("=" * 60)
        print("\n你现在可以:")
        print("  • 运行 python test_bedrock_agent.py")
        print("  • 运行 python example_bedrock.py")
        print("  • 在你的项目中使用 Bedrock")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ 导入错误: {e}")
        print("\n解决方案:")
        if "boto3" in str(e):
            print("  pip install boto3")
        else:
            print("  pip install -e pkg/HelloAgents")
        return False
        
    except Exception as e:
        print(f"\n❌ 配置错误: {e}")
        print("\n请检查:")
        print("  1. boto3 是否已安装: pip install boto3")
        print("  2. AWS credentials 是否配置:")
        print("     - 运行 'aws configure'")
        print("     - 或在 .env 中设置 AWS_ACCESS_KEY_ID 和 AWS_SECRET_ACCESS_KEY")
        print("  3. 是否有 Bedrock 访问权限:")
        print("     - 访问 https://console.aws.amazon.com/bedrock/")
        print("     - 在 'Model access' 中请求访问 Claude 模型")
        print("  4. .env 文件中是否设置:")
        print("     LLM_BASE_URL=bedrock")
        print("     AWS_REGION=us-east-1")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)



