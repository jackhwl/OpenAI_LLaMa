import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnablePassthrough
from langchain_community.utils.math import cosine_similarity
import numpy as np
from langchain_aws import ChatBedrockConverse

# 1. 定义路由描述
sichuan_route_prompt = "你是一位处理川菜的专家。用户的问题是关于麻辣、辛香、重口味的菜肴，例如水煮鱼、麻婆豆腐、鱼香肉丝、宫保鸡丁、花椒、海椒等。"
cantonese_route_prompt = "你是一位处理粤菜的专家。用户的问题是关于清淡、鲜美、原汁原味的菜肴，例如白切鸡、老火靓汤、虾饺、云吞面等。"

route_prompts = [sichuan_route_prompt, cantonese_route_prompt]
route_names = ["川菜", "粤菜"]

# 初始化嵌入模型，并对路由描述进行向量化
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
route_prompt_embeddings = embeddings.embed_documents(route_prompts)
print(f"已定义 {len(route_names)} 个路由: {', '.join(route_names)}")

# 2. 定义不同路由的目标链
# llm = ChatDeepSeek(
#     model="deepseek-chat", 
#     temperature=0, 
#     api_key=os.getenv("DEEPSEEK_API_KEY")
#     )
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0.1,
    max_tokens=4096
)
# 定义川菜和粤菜处理链
sichuan_chain = (
    PromptTemplate.from_template("你是一位川菜大厨。请用正宗的川菜做法，回答关于「{query}」的问题。")
    | llm
    | StrOutputParser()
)
cantonese_chain = (
    PromptTemplate.from_template("你是一位粤菜大厨。请用经典的粤菜做法，回答关于「{query}」的问题。")
    | llm
    | StrOutputParser()
)

route_map = { "川菜": sichuan_chain, "粤菜": cantonese_chain }
print("川菜和粤菜的处理链创建成功。\n")

# 3. 创建路由函数
def route(info):
    # 对用户查询进行嵌入
    query_embedding = embeddings.embed_query(info["query"])
    
    # 计算与各路由提示的余弦相似度
    similarity_scores = cosine_similarity([query_embedding], route_prompt_embeddings)[0]
    
    # 找到最相似的路由
    chosen_route_index = np.argmax(similarity_scores)
    chosen_route_name = route_names[chosen_route_index]
    
    print(f"路由决策: 检测到问题与“{chosen_route_name}”最相似。")
    
    # 获取对应的处理链
    chosen_chain = route_map[chosen_route_name]
    
    # 直接调用选中的链并返回结果
    return chosen_chain.invoke(info)

# 创建完整的路由链
full_chain = RunnableLambda(route)


# 4. 运行演示查询
demo_queries = [
    "水煮鱼怎么做才嫩？",        # 应该路由到川菜
    "如何做一碗清淡的云吞面？",    # 应该路由到粤菜
    "麻婆豆腐的核心调料是什么？",  # 应该路由到川菜
]

for i, query in enumerate(demo_queries, 1):
    print(f"\n--- 问题 {i}: {query} ---")
    try:
        # 传入字典，full_chain 会直接返回最终答案
        result = full_chain.invoke({"query": query})
        print(f"回答: {result}")
    except Exception as e:
        print(f"执行错误: {e}")

