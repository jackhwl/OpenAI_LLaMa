import os
import time
import torch
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock

load_dotenv()

markdown_path = "./easy-rl-chapter1.md"

# 加载本地markdown文件
print("📄 加载 Markdown 文件...")
loader = UnstructuredMarkdownLoader(markdown_path)
docs = loader.load()

# 文本分块
print("✂️  文本分块...")
text_splitter = RecursiveCharacterTextSplitter()
chunks = text_splitter.split_documents(docs)
print(f"   分块数量: {len(chunks)}")

# 提示词模板
prompt = ChatPromptTemplate.from_template("""请根据下面提供的上下文信息来回答问题。
请确保你的回答完全基于这些上下文。
如果上下文中没有足够的信息来回答问题，请直接告知："抱歉，我无法根据提供的上下文找到相关信息来回答此问题。"

上下文:
{context}

问题: {question}

回答:"""
                                          )

# 用户查询
question = "文中举了哪些例子？"

def benchmark_device(device_name, device):
    """对指定设备进行性能测试"""
    print(f"\n{'='*60}")
    print(f"🧪 测试设备: {device_name.upper()}")
    print(f"{'='*60}")
    
    # 强制 PyTorch 清理缓存
    if device == 'mps':
        torch.mps.empty_cache()
    elif device == 'cuda':
        torch.cuda.empty_cache()
    
    # 创建新的嵌入模型（不使用之前的缓存）
    start_time = time.time()
    print(f"⏱️  创建嵌入模型...")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={'device': device},
        encode_kwargs={'normalize_embeddings': True}
    )
    model_load_time = time.time() - start_time
    print(f"   模型加载时间: {model_load_time:.2f} 秒")
    
    # 构建向量存储并添加文档（这是最耗时的部分）
    start_time = time.time()
    print(f"🔢 计算文档嵌入向量 (共 {len(chunks)} 个文档)...")
    vectorstore = InMemoryVectorStore(embeddings)
    vectorstore.add_documents(chunks)
    embedding_time = time.time() - start_time
    print(f"   ✅ 嵌入计算时间: {embedding_time:.2f} 秒")
    
    # 执行查询
    start_time = time.time()
    print(f"🔍 执行相似度搜索...")
    retrieved_docs = vectorstore.similarity_search(question, k=3)
    search_time = time.time() - start_time
    print(f"   ✅ 搜索时间: {search_time:.2f} 秒")
    
    # 总时间
    total_time = model_load_time + embedding_time + search_time
    print(f"\n📊 总耗时: {total_time:.2f} 秒")
    print(f"   - 模型加载: {model_load_time:.2f}s")
    print(f"   - 嵌入计算: {embedding_time:.2f}s (关键指标)")
    print(f"   - 相似度搜索: {search_time:.2f}s")
    
    return {
        'device': device_name,
        'model_load_time': model_load_time,
        'embedding_time': embedding_time,
        'search_time': search_time,
        'total_time': total_time
    }

# 运行基准测试
results = []

print("\n" + "="*60)
print("🚀 开始 CPU vs MPS 性能对比测试")
print("="*60)

# 测试 CPU
results.append(benchmark_device("CPU", "cpu"))

# 测试 MPS (如果可用)
if torch.backends.mps.is_available():
    results.append(benchmark_device("MPS (Apple Silicon GPU)", "mps"))
else:
    print("\n⚠️  MPS 不可用，跳过 GPU 测试")

# 显示对比结果
if len(results) > 1:
    print("\n" + "="*60)
    print("📊 性能对比总结")
    print("="*60)
    
    cpu_result = results[0]
    mps_result = results[1]
    
    speedup_embedding = cpu_result['embedding_time'] / mps_result['embedding_time']
    speedup_total = cpu_result['total_time'] / mps_result['total_time']
    
    print(f"\n嵌入计算加速比: {speedup_embedding:.2f}x")
    print(f"   CPU:  {cpu_result['embedding_time']:.2f} 秒")
    print(f"   MPS:  {mps_result['embedding_time']:.2f} 秒")
    
    print(f"\n总体加速比: {speedup_total:.2f}x")
    print(f"   CPU 总耗时:  {cpu_result['total_time']:.2f} 秒")
    print(f"   MPS 总耗时:  {mps_result['total_time']:.2f} 秒")
    
    if speedup_embedding > 1.5:
        print(f"\n🎉 MPS 显著更快! 建议使用 GPU 加速")
    elif speedup_embedding > 1.1:
        print(f"\n✅ MPS 略快，可考虑使用 GPU")
    else:
        print(f"\n⚠️  性能差异不明显，CPU 也足够")

print("\n" + "="*60)
print("✅ 基准测试完成!")
print("="*60)

