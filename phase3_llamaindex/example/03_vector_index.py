"""
==========================================
示例 3: LlamaIndex 向量索引
==========================================
学习目标：
1. 使用 VectorStoreIndex 构建索引
2. Chroma 向量库持久化
3. 索引的创建与加载
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()

KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "data" / "ai_knowledge"
CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"
COLLECTION = "ai_knowledge"


def get_embed_model():
    """配置 Embedding 模型"""

    return OpenAIEmbedding(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="text-embedding-3-small",
    )


def build_persisted_index():
    """构建并持久化向量索引"""

    docs = SimpleDirectoryReader(str(KNOWLEDGE_DIR)).load_data()
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = splitter.get_nodes_from_documents(docs)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    db = chromadb.PersistentClient(path=str(CHROMA_DIR))
    chroma_collection = db.get_or_create_collection(COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=get_embed_model(),
    )
    print(f"=== 索引已持久化到 {CHROMA_DIR} ===\n")
    return index


def load_existing_index():
    """从 Chroma 加载已有索引"""

    db = chromadb.PersistentClient(path=str(CHROMA_DIR))
    chroma_collection = db.get_or_create_collection(COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=get_embed_model(),
    )


def demo_query(index):
    """简单检索验证"""

    retriever = index.as_retriever(similarity_top_k=2)
    nodes = retriever.retrieve("RAG 是什么")
    print("=== 检索结果 ===\n")
    for i, node in enumerate(nodes, 1):
        print(f"{i}. 分数: {node.score:.4f}")
        print(f"   {node.text[:120]}...\n")


if __name__ == "__main__":
    print("🚀 示例 3: LlamaIndex 向量索引\n")

    if CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()):
        print("从已有 Chroma 加载索引...\n")
        idx = load_existing_index()
    else:
        idx = build_persisted_index()
    demo_query(idx)

    print("✅ 示例运行完成！")
