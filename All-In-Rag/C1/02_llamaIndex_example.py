import os
import torch
# os.environ['HF_ENDPOINT']='https://hf-mirror.com'
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings 
# from llama_index.llms.deepseek import DeepSeek
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

# Settings.llm = DeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))
# Settings.embed_model = HuggingFaceEmbedding("BAAI/bge-small-zh-v1.5")

# 自动检测最佳设备：MPS (Apple Silicon GPU) > CUDA > CPU
if torch.backends.mps.is_available():
    device = 'mps'
    print(f"✅ 使用 Apple Silicon GPU (MPS)")
elif torch.cuda.is_available():
    device = 'cuda'
    print(f"✅ 使用 NVIDIA GPU (CUDA)")
else:
    device = 'cpu'
    print(f"⚠️  使用 CPU")

# 配置 AWS Bedrock LLM
Settings.llm = BedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0.7,
    max_tokens=4096
)

# 配置嵌入模型 - 使用 GPU 加速
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-zh-v1.5",
    device=device
)

docs = SimpleDirectoryReader(input_files=["./easy-rl-chapter1.md"]).load_data()

index = VectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()

print(query_engine.get_prompts())
response = query_engine.query("文中举了哪些例子?")
print(f"\n💬 回答:\n{response}")
