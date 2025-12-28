import json
import os
import numpy as np
import torch
from transformers import AutoModel, AutoProcessor
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from pymilvus import connections, MilvusClient, FieldSchema, CollectionSchema, DataType, Collection, AnnSearchRequest, RRFRanker

# 1. 初始化设置
COLLECTION_NAME = "dragon_siglip_demo"
MILVUS_URI = "http://localhost:19530"  # 服务器模式
DATA_PATH = "../data/C4/metadata/dragon.json"  # 相对路径
BATCH_SIZE = 50

# 2. 自定义SigLIP嵌入函数类
class SigLIPEmbeddingFunction:
    def __init__(self, model_name="google/siglip-base-patch16-256-multilingual", device="cpu"):
        """
        初始化SigLIP嵌入函数
        Args:
            model_name: SigLIP模型名称
            device: 设备类型 ("cpu" 或 "cuda")
        """
        self.model_name = model_name
        self.device = device
        
        print(f"--> 正在加载 SigLIP 模型: {model_name}")
        self.model = AutoModel.from_pretrained(model_name)
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model.to(device)
        self.model.eval()
        
        # 初始化TF-IDF作为稀疏向量生成器
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=10000,  # 限制词汇表大小以节省空间
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.tfidf_fitted = False
        
        # 获取文本编码器的输出维度
        with torch.no_grad():
            dummy_text = ["test"]
            inputs = self.processor(text=dummy_text, padding="max_length", return_tensors="pt")
            outputs = self.model.text_model(**{k: v.to(device) for k, v in inputs.items() if k != 'pixel_values'})
            self.dense_dim = outputs.pooler_output.shape[-1]
        
        print(f"--> SigLIP 模型加载完成。密集向量维度: {self.dense_dim}")
    
    @property
    def dim(self):
        """返回维度信息，兼容原BGE-M3接口"""
        return {
            "dense": self.dense_dim,
            "sparse": self.tfidf_vectorizer.max_features if self.tfidf_fitted else 10000
        }
    
    def fit_sparse(self, docs):
        """拟合稀疏向量模型（TF-IDF）"""
        print("--> 正在拟合 TF-IDF 模型...")
        self.tfidf_vectorizer.fit(docs)
        self.tfidf_fitted = True
        print(f"--> TF-IDF 模型拟合完成。词汇表大小: {len(self.tfidf_vectorizer.vocabulary_)}")
    
    def encode_text_dense(self, texts):
        """使用SigLIP编码文本为密集向量"""
        if isinstance(texts, str):
            texts = [texts]
        
        dense_vectors = []
        batch_size = 8  # 减小批次大小以节省内存
        
        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                inputs = self.processor(text=batch_texts, padding="max_length", truncation=True, return_tensors="pt")
                inputs = {k: v.to(self.device) for k, v in inputs.items() if k != 'pixel_values'}
                
                outputs = self.model.text_model(**inputs)
                embeddings = outputs.pooler_output
                
                # 归一化向量
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                dense_vectors.extend(embeddings.cpu().numpy())
        
        return np.array(dense_vectors)
    
    def encode_text_sparse(self, texts):
        """使用TF-IDF编码文本为稀疏向量"""
        if not self.tfidf_fitted:
            raise ValueError("请先调用 fit_sparse() 方法拟合TF-IDF模型")
        
        if isinstance(texts, str):
            texts = [texts]
        
        sparse_matrix = self.tfidf_vectorizer.transform(texts)
        return sparse_matrix
    
    def __call__(self, texts):
        """主调用方法，返回密集和稀疏向量"""
        if isinstance(texts, str):
            texts = [texts]
        
        # 如果还没有拟合稀疏模型，先拟合
        if not self.tfidf_fitted:
            self.fit_sparse(texts)
        
        dense_vectors = self.encode_text_dense(texts)
        sparse_vectors = self.encode_text_sparse(texts)
        
        return {
            "dense": dense_vectors,
            "sparse": sparse_vectors
        }

# 3. 连接 Milvus 并初始化嵌入模型
print(f"--> 正在连接到 Milvus: {MILVUS_URI}")
connections.connect(uri=MILVUS_URI)

print("--> 正在初始化 SigLIP 嵌入模型...")
ef = SigLIPEmbeddingFunction(device="cpu")  # 如果有GPU可以改为"cuda"

# 4. 创建 Collection
milvus_client = MilvusClient(uri=MILVUS_URI)
if milvus_client.has_collection(COLLECTION_NAME):
    print(f"--> 正在删除已存在的 Collection '{COLLECTION_NAME}'...")
    milvus_client.drop_collection(COLLECTION_NAME)

fields = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
    FieldSchema(name="img_id", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="path", dtype=DataType.VARCHAR, max_length=256),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=256),
    FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=4096),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="location", dtype=DataType.VARCHAR, max_length=128),
    FieldSchema(name="environment", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
    FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=ef.dim["dense"])
]

# 如果集合不存在，则创建它及索引
if not milvus_client.has_collection(COLLECTION_NAME):
    print(f"--> 正在创建 Collection '{COLLECTION_NAME}'...")
    schema = CollectionSchema(fields, description="使用SigLIP的龙混合检索示例")
    # 创建集合
    collection = Collection(name=COLLECTION_NAME, schema=schema, consistency_level="Strong")
    print("--> Collection 创建成功。")

    # 5. 创建索引
    print("--> 正在为新集合创建索引...")
    sparse_index = {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"}
    collection.create_index("sparse_vector", sparse_index)
    print("稀疏向量索引创建成功。")

    dense_index = {"index_type": "AUTOINDEX", "metric_type": "IP"}
    collection.create_index("dense_vector", dense_index)
    print("密集向量索引创建成功。")

collection = Collection(COLLECTION_NAME)

# 6. 加载数据并插入
collection.load()
print(f"--> Collection '{COLLECTION_NAME}' 已加载到内存。")

if collection.is_empty:
    print(f"--> Collection 为空，开始插入数据...")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"数据文件未找到: {DATA_PATH}")
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    docs, metadata = [], []
    for item in dataset:
        parts = [
            item.get('title', ''),
            item.get('description', ''),
            item.get('location', ''),
            item.get('environment', ''),
            # *item.get('combat_details', {}).get('combat_style', []),
            # *item.get('combat_details', {}).get('abilities_used', []),
            # item.get('scene_info', {}).get('time_of_day', '')
        ]
        docs.append(' '.join(filter(None, parts)))
        metadata.append(item)
    print(f"--> 数据加载完成，共 {len(docs)} 条。")

    print("--> 正在生成向量嵌入...")
    embeddings = ef(docs)
    print("--> 向量生成完成。")

    print("--> 正在分批插入数据...")
    # 为每个字段准备批量数据
    img_ids = [doc["img_id"] for doc in metadata]
    paths = [doc["path"] for doc in metadata]
    titles = [doc["title"] for doc in metadata]
    descriptions = [doc["description"] for doc in metadata]
    categories = [doc["category"] for doc in metadata]
    locations = [doc["location"] for doc in metadata]
    environments = [doc["environment"] for doc in metadata]
    
    # 获取向量 - 注意SigLIP返回的格式与BGE-M3不同
    sparse_vectors = []
    dense_vectors = embeddings["dense"].tolist()
    
    # 将稀疏矩阵转换为Milvus可接受的格式
    sparse_matrix = embeddings["sparse"]
    for i in range(sparse_matrix.shape[0]):
        row = sparse_matrix.getrow(i)
        # 创建稀疏向量字典格式
        sparse_dict = {}
        for j in range(row.nnz):
            sparse_dict[row.indices[j]] = float(row.data[j])
        sparse_vectors.append(sparse_dict)
    
    # 插入数据
    collection.insert([
        img_ids,
        paths,
        titles,
        descriptions,
        categories,
        locations,
        environments,
        sparse_vectors,
        dense_vectors
    ])
    
    collection.flush()
    print(f"--> 数据插入完成，总数: {collection.num_entities}")
else:
    print(f"--> Collection 中已有 {collection.num_entities} 条数据，跳过插入。")

# 7. 执行搜索
search_query = "悬崖上的巨龙"
search_filter = 'category in ["western_dragon", "chinese_dragon", "movie_character"]'
top_k = 5

print(f"\n{'='*20} 开始混合搜索 {'='*20}")
print(f"查询: '{search_query}'")
print(f"过滤器: '{search_filter}'")

# 生成查询向量
query_embeddings = ef([search_query])
dense_vec = query_embeddings["dense"][0].tolist()

# 处理稀疏向量
sparse_matrix = query_embeddings["sparse"]
sparse_row = sparse_matrix.getrow(0)
sparse_dict = {}
for j in range(sparse_row.nnz):
    sparse_dict[sparse_row.indices[j]] = float(sparse_row.data[j])

# 打印向量信息
print("\n=== 向量信息 ===")
print(f"密集向量维度: {len(dense_vec)}")
print(f"密集向量前5个元素: {dense_vec[:5]}")
print(f"密集向量范数: {np.linalg.norm(dense_vec):.4f}")

print(f"\n稀疏向量维度: {sparse_matrix.shape[1]}")
print(f"稀疏向量非零元素数量: {sparse_row.nnz}")
print("稀疏向量前5个非零元素:")
for i, (idx, val) in enumerate(list(sparse_dict.items())[:5]):
    print(f"  - 索引: {idx}, 值: {val:.4f}")
density = (sparse_row.nnz / sparse_matrix.shape[1] * 100)
print(f"\n稀疏向量密度: {density:.8f}%")

# 定义搜索参数
search_params = {"metric_type": "IP", "params": {}}

# 先执行单独的搜索
print("\n--- [单独] 密集向量搜索结果 ---")
dense_results = collection.search(
    [dense_vec],
    anns_field="dense_vector",
    param=search_params,
    limit=top_k,
    expr=search_filter,
    output_fields=["title", "path", "description", "category", "location", "environment"]
)[0]

for i, hit in enumerate(dense_results):
    print(f"{i+1}. {hit.entity.get('title')} (Score: {hit.distance:.4f})")
    print(f"    路径: {hit.entity.get('path')}")
    print(f"    描述: {hit.entity.get('description')[:100]}...")

print("\n--- [单独] 稀疏向量搜索结果 ---")
sparse_results = collection.search(
    [sparse_dict],
    anns_field="sparse_vector",
    param=search_params,
    limit=top_k,
    expr=search_filter,
    output_fields=["title", "path", "description", "category", "location", "environment"]
)[0]

for i, hit in enumerate(sparse_results):
    print(f"{i+1}. {hit.entity.get('title')} (Score: {hit.distance:.4f})")
    print(f"    路径: {hit.entity.get('path')}")
    print(f"    描述: {hit.entity.get('description')[:100]}...")

print("\n--- [混合] 稀疏+密集向量搜索结果 ---")
# 创建 RRF 融合器
rerank = RRFRanker(k=60)

# 创建搜索请求
dense_req = AnnSearchRequest([dense_vec], "dense_vector", search_params, limit=top_k)
sparse_req = AnnSearchRequest([sparse_dict], "sparse_vector", search_params, limit=top_k)

# 执行混合搜索
results = collection.hybrid_search(
    [sparse_req, dense_req],
    rerank=rerank,
    limit=top_k,
    output_fields=["title", "path", "description", "category", "location", "environment"]
)[0]

# 打印最终结果
for i, hit in enumerate(results):
    print(f"{i+1}. {hit.entity.get('title')} (Score: {hit.distance:.4f})")
    print(f"    路径: {hit.entity.get('path')}")
    print(f"    描述: {hit.entity.get('description')[:100]}...")

# 8. 清理资源
milvus_client.release_collection(collection_name=COLLECTION_NAME)
print(f"已从内存中释放 Collection: '{COLLECTION_NAME}'")
milvus_client.drop_collection(COLLECTION_NAME)
print(f"已删除 Collection: '{COLLECTION_NAME}'")