## All-in-RAG | 大模型应用开发实战一：RAG技术全栈指南
  - https://github.com/datawhalechina/all-in-rag
    pyenv local 3.12.7
    python -m venv .v3127
    source venv/bin/activate
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
