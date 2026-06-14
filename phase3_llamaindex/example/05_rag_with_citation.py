"""
==========================================
示例 5: LlamaIndex RAG 引用来源
==========================================
学习目标：
1. 查询时展示 source nodes
2. 在回答中标注引用文件名
3. 提高 RAG 回答的可追溯性
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
    """配置 LLM 与 Embedding"""

    Settings.llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0.2,
    )
    Settings.embed_model = OpenAIEmbedding(api_key=os.getenv("OPENAI_API_KEY"))


def build_citation_engine():
    """构建带引用展示的查询引擎"""

    docs = SimpleDirectoryReader(str(KNOWLEDGE_DIR)).load_data()
    nodes = SentenceSplitter(chunk_size=512, chunk_overlap=50).get_nodes_from_documents(docs)
    index = VectorStoreIndex(nodes)
    return index.as_query_engine(similarity_top_k=3)


def format_source(node):
    """格式化来源信息"""

    file_name = node.metadata.get("file_name", "未知来源")
    score = f"{node.score:.4f}" if node.score else "N/A"
    return f"[{file_name}] (相关度: {score})"


def query_with_citation(engine, question):
    """查询并打印回答与引用"""

    print(f"=== 问题: {question} ===\n")
    response = engine.query(question)
    print(f"回答:\n{response}\n")
    print("引用来源:")
    for i, node in enumerate(response.source_nodes, 1):
        print(f"  {i}. {format_source(node)}")
        print(f"     片段: {node.text[:100]}...")
    print()


if __name__ == "__main__":
    print("🚀 示例 5: LlamaIndex RAG 引用来源\n")

    configure_settings()
    engine = build_citation_engine()
    query_with_citation(engine, "AI Agent 有哪些关键能力？")

    print("✅ 示例运行完成！")
