# Phase 3: LlamaIndex

学习 LlamaIndex 框架，深入掌握数据索引和检索增强生成（RAG）技术。

## 学习目标

完成本阶段后，你将能够：

- ✅ 理解 LlamaIndex 的核心架构
- ✅ 使用 Document Loaders 加载各种数据源
- ✅ 使用 Node Parser 和 Text Splitter 分段文档
- ✅ 构建向量索引（Vector Store Index）
- ✅ 实现高级查询（Query Engine）
- ✅ 深入理解 RAG 工作原理
- ✅ 优化 RAG 性能和准确性

## 前置条件

1. ✅ 已完成 Phase 2（LangChain）
2. 已在项目根目录配置 `.env` 文件
3. 已安装阶段依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 目录结构

```
phase3_llamaindex/
├── example/               # AI 生成的示例代码
│   ├── 01_document_loader.py          # 文档加载
│   ├── 02_text_splitter.py            # 文本分段
│   ├── 03_vector_index.py             # 向量索引
│   ├── 04_query_engine.py             # 查询引擎
│   ├── 05_rag_basic.py                # RAG 基础
│   ├── 06_rag_advanced.py             # RAG 高级（重排序、混合检索）
│   ├── 07_data_sources.py             # 多数据源集成
│   └── 08_reranking.py                # 结果重排序
├── practice/              # 手动练习代码
├── notes/                 # 学习笔记
│   ├── 01_architecture.md
│   ├── 02_indexing.md
│   ├── 03_querying.md
│   ├── 04_rag_optimization.md
│   └── 05_best_practices.md
├── tests/                 # 测试文件
├── config/                # 配置文件
└── requirements.txt       # 本阶段依赖
```

## LlamaIndex 核心概念

### 1. Data Connectors（数据连接器）

从各种数据源加载文档。

```python
from llama_index import SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
```

### 2. Indices（索引）

将文档转换为可查询的格式。

```python
from llama_index import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)
```

### 3. Query Engines（查询引擎）

对索引进行查询。

```python
query_engine = index.as_query_engine()
response = query_engine.query("什么是 AI Agent？")
```

### 4. Chat Engines（对话引擎）

基于上下文的对话查询。

```python
chat_engine = index.as_chat_engine()
response = chat_engine.chat("再详细说明一下")
```

## 学习路径

### 第 1 步：Document Loaders

**示例代码：** `example/01_document_loader.py`

**学习重点：**
- 加载各种文件格式（PDF、TXT、Markdown）
- 从网页抓取内容
- 从数据库加载数据

### 第 2 步：Text Splitting

**示例代码：** `example/02_text_splitter.py`

**学习重点：**
- Node Parser 原理
- 不同的分割策略
- 保留语义完整性

### 第 3 步：Vector Index

**示例代码：** `example/03_vector_index.py`

**学习重点：**
- Embeddings 原理
- 向量存储
- 相似度搜索

### 第 4 步：Query Engine

**示例代码：** `example/04_query_engine.py`

**学习重点：**
- 不同查询策略
- 响应合成（Response Synthesizer）
- 自定义查询配置

### 第 5 步：RAG 基础

**示例代码：** `example/05_rag_basic.py`

**学习重点：**
- RAG 完整流程
- 端到端实现
- 性能评估

### 第 6 步：RAG 高级优化

**示例代码：** `example/06_rag_advanced.py`

**学习重点：**
- 混合检索（Hybrid Search）
- 重排序（Reranking）
- 多路查询（Multi-query）

## 运行示例

```bash
# 进入阶段目录
cd phase3_llamaindex

# 运行特定示例
python example/01_document_loader.py

# 运行所有测试
pytest tests/
```

## RAG vs 直接问答

| 特性 | RAG | 直接问答 |
|------|-----|----------|
| 知识来源 | 外部文档 | 模型训练数据 |
| 实时性 | 实时更新 | 依赖训练时间 |
| 准确性 | 可验证 | 可能幻觉 |
| 成本 | 较低（小模型） | 较高（大模型） |
| 适用场景 | 企业知识库、问答系统 | 通用对话 |

## 常见问题

### 1. 检索结果不相关？

**解决方案：**
- 调整 `similarity_top_k` 参数
- 优化文本分段策略
- 使用更好的 Embeddings 模型
- 添加重排序（Reranking）

### 2. 响应包含幻觉？

**解决方案：**
- 限制回答仅基于检索内容
- 使用 `Response Mode` 控制生成方式
- 添加引用（Citations）

### 3. 性能太慢？

**解决方案：**
- 使用本地向量数据库
- 优化 `chunk_size` 和 `chunk_overlap`
- 缓存查询结果
- 使用异步查询

## 下一步

完成本阶段后，进入 **Phase 4: AutoGen**，学习多智能体协作。

---

**开始学习吧！** 🦙
