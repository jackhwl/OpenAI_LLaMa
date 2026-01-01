## All-in-RAG | 大模型应用开发实战一：RAG技术全栈指南
  - https://github.com/datawhalechina/all-in-rag
    pyenv local 3.12.7
    python -m venv .v3127
    source .v3127/bin/activate
    pip install -r requirements.txt
  - 第一部分：RAG基础入门
    - 第一章 解锁RAG 📖 查看章节
      - 第一节 RAG简介 - RAG技术概述与应用场景
        - 初级 RAG（Naive RAG）	
        - 高级 RAG（Advanced RAG）	
        - 模块化 RAG（Modular RAG）
        - 为什么要使用 RAG？
        - RAG 已死？
      - 第二节 准备工作
      - 第三节 四步构建RAG
        - 一、启动虚拟环境
        - 二、运行RAG示例代码
        - 三、基于LangChain框架的RAG实现
          - 3.1 初始化设置
          - 3.2 数据准备 (Data Preparation)
          - 3.3 索引构建 (Index Construction)
          - 3.4 查询与检索 (Query and Retrieval)
          - 3.5 生成集成 (Generation Integration)
        - 四、低代码（基于LlamaIndex）
    - 第二章 数据准备
      - 第一节 数据加载
        - Garbage In, Garbage Out
        - 一、文档加载器
        - 当前主流RAG文档加载器

          | 工具名称 | 特点 | 适用场景 | 性能表现 |
          |---------|---------|---------|---------|
          | **PyMuPDF4LLM** | PDF→Markdown转换，OCR+表格识别 | 科研文献、技术手册 | 开源免费，GPU加速 |
          | **TextLoader** | 基础文本文件加载 | 纯文本处理 | 轻量高效 |
          | **DirectoryLoader** | 批量目录文件处理 | 混合格式文档库 | 支持多格式扩展 |
          | **Unstructured** | 多格式文档解析 | PDF、Word、HTML等 | 统一接口，智能解析 |
          | **FireCrawlLoader** | 网页内容抓取 | 在线文档、新闻 | 实时内容获取 |
          | **LlamaParse** | 深度PDF结构解析 | 法律合同、学术论文 | 解析精度高，商业API |
          | **Docling** | 模块化企业级解析 | 企业合同、报告 | IBM生态兼容 |
          | **Marker** | PDF→Markdown，GPU加速 | 科研文献、书籍 | 专注PDF转换 |
          | **MinerU** | 多模态集成解析 | 学术文献、财务报表 | 集成LayoutLMv3+YOLOv8 |

        - 二、Unstructured文档处理库
        - 三、从LangChain封装到原始Unstructured
          - [**Unstructured官方文档**](https://docs.unstructured.io/open-source/core-functionality/partitioning)
      - 第二节 文本分块
        - 一、理解文本分块
        - 二、文本分块重要性
          - 2.1 满足模型上下文限制
          - 2.2 为何“块”不是越大越好
        - 三、基础分块策略
          - 3.1 固定大小分块 (段落感知的自适应分块)
          - 3.2 递归字符分块 (RecursiveCharacterTextSplitter)
          - 3.3 语义分块
          - 3.4 基于文档结构的分块
        - 四、其他开源框架中的分块策略
          - 4.1 Unstructured：基于文档元素的智能分块
          - 4.2 LlamaIndex：面向节点的解析与转换
          - 4.3 ChunkViz：简易的可视化分块工具
  - 第二部分：索引构建与优化
    - 第三章 索引构建
      - 第一节 向量嵌入
        - 一、向量嵌入基础
        - 二、Embedding 技术发展
        - 三、嵌入模型训练原理
        - 四、嵌入模型选型指南
      - 第二节 多模态嵌入
        - 一、为什么需要多模态嵌入？
        - 二、CLIP 模型浅析
        - 三、常用多模态嵌入模型(以bge-visualized-m3为例)
        - 四、代码示例
          - 4.2 基础示例
      - 第三节 向量数据库
        - 一、向量数据库的作用
        - 二、工作原理
        - 三、主流向量数据库介绍
          - Pinecone
          - Milvus
          - Qdrant
          - Weaviate
          - Chroma
        - 四、本地向量存储：以 FAISS 为例
      - 第四节 Milvus介绍及多模态检索实践
        - 一、简介
        - 二、 部署安装
          - 1. 环境准备
          - 2. 下载并启动 Milvus
          - 3. 验证安装
          - 4. 常用管理命令
        - 三、核心组件
          - 3.1 Collection
            - Collection
            - Partition
            - Schema
            - Entity
            - Alias
          - 3.2 索引（index）

            | 场景 | 推荐索引 | 备注 |
            | :--- | :--- | :--- |
            | 数据可完全载入内存，追求低延迟 | **HNSW** | 内存占用较大，但查询性能和召回率都很优秀。 |
            | 数据可完全载入内存，追求高吞吐 | **IVF_FLAT / IVF_SQ8** | 性能和资源消耗的平衡之选。 |
            | 数据量巨大，无法载入内存 | **DiskANN** | 在 SSD 上性能优异，专为海量数据设计。 |
            | 追求 100% 准确率，数据量不大 | **FLAT** | 暴力搜索，确保结果最精确。 |

          - 3.3 检索
            - 3.3.1 基础向量检索 (ANN Search)
            - 3.3.2 增强检索
        - 四、milvus多模态实践
      - 第五节 索引优化
        - 一、上下文扩展
          - 句子窗口检索（Sentence Window Retrieval）
        - 二、结构化索引
          - 2.1 代码实现：基于多表格的递归检索
        - 题外话：关于框架
  - 第三部分：检索技术进阶
    - 第四章 检索优化
      - 第一节：混合检索
        - 一、稀疏向量 vs 密集向量
          - 1.1 稀疏向量 BM25, 无法理解语义, pro: 精确性
          - 1.2 密集向量 Embedding 理解语义  pro: 泛化性
          - 1.3 实例对比
        - 二、混合检索
          - 2.1 技术原理与融合方法
          - 2.2 优势与局限
        - 三、代码实践：通过 Milvus 实现混合检索
      - 第二节：查询构建
        - 一、文本到元数据过滤器
        - 二、文本到Cypher
          - 2.1 什么是 Cypher？
          - 2.2 “文本到Cypher”的原理
      - 第三节：文本到SQL
        - 一、业务挑战
        - 二、优化策略
        - 三、实现一个简单的Text2SQL框架
          - 3.1 知识库模块 (knowledge_base.py)
          - 3.2 SQL生成模块 (sql_generator.py)
          - 3.3 代理模块 (text2sql_agent.py)
          - 3.4 完整流程模拟
          - 3.5 代码运行
          - 3.6 为什么不直接使用封装好的框架？
      - 第四节：查询重构与分发
        - 一、查询翻译
          - 1.1 提示工程
          - 1.2 多查询分解 (Multi-query)
          - 1.3 退步提示（Step-Back Prompting）
          - 1.4 假设性文档嵌入 (HyDE)
        - 二、查询路由
          - 2.1 应用场景
          - 2.2 实现方法
            - 2.2.1 基于LLM的意图识别
            - 2.2.2 嵌入相似性路由
          - 2.3 LlamaIndex 拓展
      - 第五节：检索进阶
        - 一、重排序 (Re-ranking)
          - 1.1 RRF (Reciprocal Rank Fusion)
          - 1.2 RankLLM / LLM-based Reranker
          - 1.3 Cross-Encoder 重排
          - 1.4 ColBERT 重排
          - 1.5 重排方法对比
        - 二、压缩 (Compression)
          - 2.1 LangChain 的 ContextualCompressionRetriever
          - 2.2 自定义重排器与压缩管道
          - 2.3 LlamaIndex 中的检索压缩
        - 三、校正 (Correcting)
          - 校正检索（Corrective-RAG, C-RAG）
  - 第四部分：生成与评估
    - 第七章 高级RAG架构（拓展部分）
      - 第一节：基于知识图谱的RAG
        - 一、从传统RAG到知识图谱增强RAG的演进
          - 1.1 传统RAG框架的固有局限性
          - 1.2 知识图谱赋能 RAG 的核心优势
          - 1.3 GraphRAG：一种范式革新
        - 二、GraphRAG框架的核心架构与工作流程
          - 2.1 通用架构三阶段
          - 2.2 方法论分类
        - 三、前沿GraphRAG框架介绍（截至2025年）
          - 3.1 GraphRAG (Microsoft)
          - 3.2 LightRAG
          - 3.3 FRAG (Flexible RAG)
          - 3.4 GraphIRAG (Iterative Knowledge Retrieval)
        - 四、性能评估与基准测试
        - 五、生产环境部署实践与挑战
  - 第五部分：高级应用与实战
    - 第八章 项目实战一
      - 第一节 环境配置与项目架构
        - 一、项目背景
        - 二、环境配置
        - 三、项目架构
          - 3.1 项目目标
          - 3.2 数据分析
            - 3.2.1 文档分析
            - 3.2.2 结构分块局限
          - 3.3 整体架构
