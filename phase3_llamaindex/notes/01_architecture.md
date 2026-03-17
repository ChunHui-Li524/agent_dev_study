# LlamaIndex 架构笔记

## LlamaIndex 是什么？

LlamaIndex（原名 GPT Index）是一个专注于**数据索引和检索增强生成（RAG）**的框架。它帮助你将私有数据与大语言模型连接起来。

## 核心架构

```
用户查询
   ↓
Query Engine
   ↓
Retrieval（检索）
   ↓
Vector Index（向量索引）
   ↓
Document Store（文档存储）
```

## 六级架构

### 1. L0（最简单）：直接查询

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("问题")
```

### 2. L1：高级查询配置

```python
from llama_index.core.query_engine import VectorStoreIndexQueryEngine

query_engine = VectorStoreIndexQueryEngine(
    index=index,
    similarity_top_k=5,
    response_mode="compact"
)
```

### 3. L2：自定义检索和合成

```python
from llama_index.core import VectorStoreIndex, get_response_synthesizer

# 自定义检索器
retriever = index.as_retriever(
    similarity_top_k=3
)

# 自响应合成器
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize"
)

# 组合成查询引擎
from llama_index.core.query_engine import RetrieverQueryEngine

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer
)
```

### 4. L3：自定义节点后处理

```python
from llama_index.core.postprocessor import SimilarityPostprocessor

# 添加后处理器
query_engine = index.as_query_engine(
    node_postprocessors=[
        SimilarityPostprocessor(similarity_cutoff=0.7)
    ]
)
```

### 5. L4：混合检索

```python
from llama_index.core.retrievers import QueryFusionRetriever

# 融合多个检索器
fusion_retriever = QueryFusionRetriever(
    retrievers=[retriever1, retriever2],
    query_gen_prompt="...")
```

### 6. L5：完全自定义

构建完全自定义的检索和生成流程。

## 核心组件详解

### 1. Document（文档）

```python
from llama_index.core import Document

doc = Document(
    text="文档内容",
    metadata={
        "title": "文档标题",
        "author": "作者",
        "date": "2024-01-01"
    }
)
```

**元数据的重要性：**
- 用于过滤和检索
- 用于上下文理解
- 用于引用来源

### 2. Node（节点）

Node 是 Document 的分段版本。

```python
from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50
)

nodes = splitter.get_nodes_from_documents(documents)
```

**Node 包含：**
- `text`: 节点内容
- `metadata`: 元数据
- `embedding`: 向量表示
- `relationships`: 与其他节点的关系

### 3. Index（索引）

#### Vector Store Index（向量存储索引）

最常用的索引类型，基于语义相似度检索。

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)
```

#### 其他索引类型

- **List Index**: 线性遍历，适合小数据集
- **Tree Index**: 树形结构，层次化检索
- **Keyword Table Index**: 基于关键词检索
- **Vector Store Index**: 向量索引，最常用

### 4. Query Engine（查询引擎）

```python
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact",
    streaming=True
)
```

**Response Modes：**
- `compact`: 压缩上下文，保留最相关内容
- `refine`: 逐步优化答案
- `tree_summarize`: 树状结构总结
- `no_text`: 只返回检索到的节点

### 5. Chat Engine（对话引擎）

```python
chat_engine = index.as_chat_engine(
    chat_mode="condense_question",
    verbose=True
)
```

**Chat Modes：**
- `condense_question`: 压缩历史问题
- `context`: 保留完整对话历史
- `condense_plus_context`: 混合模式

## RAG 完整流程

### 1. 索引构建阶段

```
原始文档
   ↓
Document Loader
   ↓
Text Splitter（分段）
   ↓
Embedding（向量化）
   ↓
Vector Store（存储）
```

### 2. 查询阶段

```
用户问题
   ↓
Query Embedding（问题向量化）
   ↓
Vector Search（向量搜索）
   ↓
Top-K 相关节点
   ↓
LLM（生成回答）
   ↓
最终答案
```

## 性能优化

### 1. 文档分段优化

```python
from llama_index.core.node_parser import SemanticSplitterNodeParser

# 基于语义分段
splitter = SemanticSplitterNodeParser.from_defaults(
    embed_model="local:BAAI/bge-small-en-v1.5"
)
```

### 2. 混合检索

```python
from llama_index.core.retrievers import BM25Retriever, VectorRetriever

# BM25（关键词）+ Vector（语义）
bm25_retriever = BM25Retriever.from_defaults(index=index)
vector_retriever = VectorRetriever(index=index)
```

### 3. 重排序

```python
from llama_index.core.postprocessor import LLMRerank

reranker = LLMRerank(
    top_n=5,
    llm=OpenAI(model="gpt-3.5-turbo")
)
```

## 常见问题

### 1. Vector Store Index vs Tree Index？

- **Vector Store**: 基于语义相似度，适合问答
- **Tree Index**: 基于层次结构，适合导航

### 2. 如何选择 chunk_size？

- 太小：上下文碎片化
- 太大：包含无关信息
- 推荐：512-1024 tokens

### 3. Embeddings 选择？

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| OpenAI text-embedding-3 | 高质量 | 英文为主 |
| BGE 系列 | 开源高质量 | 中英双语 |
| E5 系列 | 强大检索能力 | 多语言 |

## 参考资源

- [LlamaIndex 官方文档](https://docs.llamaindex.ai)
- [LlamaIndex GitHub](https://github.com/run-llama/llama_index)
- [RAG 论文列表](https://github.com/kyrie1811/RAG_Survey)
