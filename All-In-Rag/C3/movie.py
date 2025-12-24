import os
import pandas as pd
from dotenv import load_dotenv
from llama_index.core.schema import IndexNode
## from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.deepseek import DeepSeek

import torch
from llama_index.core.node_parser import SentenceWindowNodeParser, SentenceSplitter
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import MetadataReplacementPostProcessor

from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.schema import QueryBundle

# from llama_index.core.schema import Response
from llama_index.core.schema import NodeWithScore, TextNode

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

load_dotenv()

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



# # 配置模型
# Settings.llm = DeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))
# Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")

def make_df_query_engine(df):
    """
    Minimal PandasQueryEngine replacement
    compatible with your LlamaIndex version.
    """
    class AttrDict(dict):
        __getattr__ = dict.get

    class SimpleDFQueryEngine(BaseQueryEngine):

        def __init__(self):
            super().__init__(callback_manager=Settings.callback_manager)

        def _query(self, query_bundle: QueryBundle):
            query_str = query_bundle.query_str

            try:
                df_1994 = df[df["年份"] == 1994]

                # ⭐ 关键逻辑分支
                if "最少" in query_str:
                    result = df_1994.sort_values("评分人数", ascending=True).head(1)
                else:  # 默认：最多
                    result = df_1994.sort_values("评分人数", ascending=False).head(1)

                text = result.to_string(index=False)

            except Exception as e:
                text = f"表格查询错误: {e}"

            node = TextNode(text=text)
            source_node = NodeWithScore(node=node, score=1.0)

            return AttrDict(
                response=text,
                source_nodes=[source_node],
            )

        async def _aquery(self, query_bundle: QueryBundle):
            return self._query(query_bundle)

        def _get_prompt_modules(self):
            return {}

    return SimpleDFQueryEngine()

# 1. 为每个工作表创建查询引擎和摘要节点
import pandas as pd

excel_file = '../data/C3/excel/movie.xlsx'
xls = pd.ExcelFile(excel_file)

df_query_engines = {}
all_nodes = []

for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    # 为当前工作表创建一个 PandasQueryEngine
    query_engine = make_df_query_engine(df) #PandasQueryEngine(df=df, llm=Settings.llm, verbose=True)
    # 为当前工作表创建一个摘要节点（IndexNode）
    year = sheet_name.replace('年份_', '')
    summary = f"这个表格包含了年份为 {year} 的电影信息，可以用来回答关于这一年电影的具体问题。"
    node = IndexNode(text=summary, index_id=sheet_name)
    all_nodes.append(node)
    # 存储工作表名称到其查询引擎的映射
    df_query_engines[sheet_name] = query_engine

# 2. 创建顶层索引（只包含摘要节点）
vector_index = VectorStoreIndex(all_nodes)

# 3. 创建递归检索器
vector_retriever = vector_index.as_retriever(similarity_top_k=1)
recursive_retriever = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever},
    query_engine_dict=df_query_engines,
    verbose=True,
)

# 4. 创建查询引擎
query_engine = RetrieverQueryEngine.from_args(recursive_retriever)

# 5. 执行查询
query = "1994年评分人数最多的电影是哪一部？"
print(f"查询: {query}")
response = query_engine.query(query)
print(f"回答: {response}")