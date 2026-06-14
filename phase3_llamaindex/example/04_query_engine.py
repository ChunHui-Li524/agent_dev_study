"""
==========================================
示例 4: LlamaIndex 查询引擎
==========================================
学习目标：
1. 从向量索引创建 Query Engine
2. 执行 RAG 问答："什么是 RAG"
3. 配置 LLM 与检索参数
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

load_dotenv()

KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "data" / "ai_knowledge"


def configure_settings():
    """配置全局 LLM 与 Embedding"""

    Settings.llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0.3,
    )
    Settings.embed_model = OpenAIEmbedding(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="text-embedding-3-small",
    )


def build_query_engine():
    """构建查询引擎"""

    docs = SimpleDirectoryReader(str(KNOWLEDGE_DIR)).load_data()
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = splitter.get_nodes_from_documents(docs)
    index = VectorStoreIndex(nodes)
    return index.as_query_engine(similarity_top_k=3)


def ask(engine, question):
    """提问并打印回答"""

    print(f"=== 问题: {question} ===\n")
    response = engine.query(question)
    print(response)
    print()


def demo_multiple_questions(engine):
    """多个问题演示"""

    questions = ["什么是 RAG", "Function Calling 的工作流程是什么？"]
    for q in questions:
        ask(engine, q)


if __name__ == "__main__":
    print("🚀 示例 4: LlamaIndex 查询引擎\n")

    configure_settings()
    query_engine = build_query_engine()
    ask(query_engine, "什么是 RAG")
    # demo_multiple_questions(query_engine)

    print("✅ 示例运行完成！")
