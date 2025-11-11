# my_llm.py
import json
import os
from typing import List, Dict, Optional
from openai import OpenAI
#from hello_agents import HelloAgentsLLM
from llm_client import HelloJackAgentsLLM


class MyLLM(HelloJackAgentsLLM):
    """
    一个自定义的LLM客户端，通过继承增加了对ModelScope的支持。
    """
    #vpass # 暂时留空

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        provider: Optional[str] = "auto",
        **kwargs
    ):
        #if provider == "auto":
        provider = self._auto_detect_provider(api_key, base_url)
        
        self.provider = provider
        self.model = model or os.getenv("LLM_MODEL_ID")
        
        # 2. 使用父类的 _resolve_credentials 解析凭证
        resolved_api_key, resolved_base_url = self._resolve_credentials(api_key, base_url)
        
        # 3. 根据 provider 创建对应的客户端
        if self.provider == "bedrock":
            print("正在使用 AWS Bedrock Provider")
            
            # resolved_base_url 包含 region 信息
            self.region = resolved_base_url
            self.temperature = kwargs.get('temperature', 0.7)
            self.timeout = kwargs.get('timeout', 60)
            
            # 设置默认模型
            if not self.model:
                self.model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            
            # 创建 Bedrock 客户端
            import boto3
            self.client = boto3.client('bedrock-runtime', region_name=self.region)
        

        # 检查provider是否为我们想处理的'modelscope'
        elif provider == "modelscope":
            print("正在使用自定义的 ModelScope Provider")
            self.provider = "modelscope"
            
            # 解析 ModelScope 的凭证
            self.api_key = api_key or os.getenv("MODELSCOPE_API_KEY")
            self.base_url = base_url or "https://api-inference.modelscope.cn/v1/"
            
            # 验证凭证是否存在
            if not self.api_key:
                raise ValueError("ModelScope API key not found. Please set MODELSCOPE_API_KEY environment variable.")

            # 设置默认模型和其他参数
            self.model = model or os.getenv("LLM_MODEL_ID") or "Qwen/Qwen2.5-VL-72B-Instruct"
            self.temperature = kwargs.get('temperature', 0.7)
            self.max_tokens = kwargs.get('max_tokens')
            self.timeout = kwargs.get('timeout', 60)
            
            # 使用获取的参数创建OpenAI客户端实例
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)

        else:
            # 如果不是 modelscope, 则完全使用父类的原始逻辑来处理
            super().__init__(model=model, api_key=api_key, base_url=base_url, provider=provider, **kwargs)

    def _convert_messages_to_bedrock_format(self, messages: List[Dict[str, str]]) -> tuple[List[Dict], Optional[str]]:
        """
        将 OpenAI 格式的消息转换为 Bedrock 格式
        返回: (bedrock_messages, system_prompt)
        """
        system_prompt = None
        bedrock_messages = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                # Bedrock 将 system 消息单独处理
                system_prompt = content
            elif role in ["user", "assistant"]:
                bedrock_messages.append({
                    "role": role,
                    "content": content
                })
        
        return bedrock_messages, system_prompt
    
    def _call_bedrock(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用 AWS Bedrock API（流式响应）
        """
        bedrock_messages, system_prompt = self._convert_messages_to_bedrock_format(messages)
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": bedrock_messages,
            "temperature": temperature
        }
        
        if system_prompt:
            body["system"] = system_prompt
        
        try:
            response = self.client.invoke_model_with_response_stream(
                modelId=self.model,
                body=json.dumps(body)
            )
            
            print("✅ 大语言模型响应成功:")
            collected_content = []
            
            # 处理流式响应
            for event in response['body']:
                chunk = json.loads(event['chunk']['bytes'])
                
                if chunk['type'] == 'content_block_delta':
                    if 'delta' in chunk and 'text' in chunk['delta']:
                        content = chunk['delta']['text']
                        print(content, end="", flush=True)
                        collected_content.append(content)
            
            print()  # 在流式输出结束后换行
            return "".join(collected_content)
            
        except Exception as e:
            print(f"❌ 调用 Bedrock API 时发生错误: {e}")
            return None
        
    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大语言模型进行思考，并返回其响应。
        重写此方法以支持 Bedrock
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        
        # 如果是 Bedrock，使用专门的方法
        if self.provider == "bedrock":
            return self._call_bedrock(messages, temperature)
        
        # 否则使用父类的方法
        return super().think(messages, temperature)