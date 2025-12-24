import os
import torch
from llama_index.core.node_parser import SentenceWindowNodeParser, SentenceSplitter
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import MetadataReplacementPostProcessor

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

# 1. 配置模型
Settings.llm = BedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0.1,
    max_tokens=4096
)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en",
    device=device
)

# 假设 Settings.llm 和 Settings.embed_model 已经预先配置好

# 1. 加载文档
documents = SimpleDirectoryReader(
    input_files=["../data/C3/pdf/IPCC_AR6_WGII_Chapter03.pdf"]
).load_data()

# 2. 创建节点与构建索引
# 2.1 句子窗口索引
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)
sentence_nodes = node_parser.get_nodes_from_documents(documents)
sentence_index = VectorStoreIndex(sentence_nodes)

# 2.2 常规分块索引 (基准)
base_parser = SentenceSplitter(chunk_size=512)
base_nodes = base_parser.get_nodes_from_documents(documents)
base_index = VectorStoreIndex(base_nodes)

# 3. 构建查询引擎
sentence_query_engine = sentence_index.as_query_engine(
    similarity_top_k=2,
    node_postprocessors=[
        MetadataReplacementPostProcessor(target_metadata_key="window")
    ],
)
base_query_engine = base_index.as_query_engine(similarity_top_k=2)

# 4. 执行查询并对比结果
query = "What are the concerns surrounding the AMOC?"
print(f"\n{'='*60}")
print(f"❓ 查询: {query}")
print(f"{'='*60}\n")

print("--- 句子窗口检索结果 ---")
window_response = sentence_query_engine.query(query)
print(f"💬 回答:\n{window_response}\n")

print("\n" + "="*60)
print("--- 常规检索结果 ---")
print("="*60)
base_response = base_query_engine.query(query)
print(f"💬 回答:\n{base_response}\n")

