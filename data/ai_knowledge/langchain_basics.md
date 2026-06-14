# LangChain 核心概念

LangChain 是构建 LLM 应用的开发框架。

## 核心组件

- **Prompt Template**：可复用提示模板
- **Chain**：组件链式组合（LCEL）
- **Memory**：对话历史管理
- **Agent**：自动选择工具并多步执行
- **Retriever**：RAG 检索接口

## 典型 RAG 链

Document Loader → Splitter → Embedding → VectorStore → Retriever → LLM
