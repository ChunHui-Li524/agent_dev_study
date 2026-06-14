"""
==========================================
示例 2: LlamaIndex 文本切分
==========================================
学习目标：
1. 使用 SentenceSplitter 切分文档
2. 对比不同 chunk_size 与 chunk_overlap
3. 理解切分策略对 RAG 的影响
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

load_dotenv()

KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "data" / "ai_knowledge"


def load_sample_docs():
    """加载示例文档"""

    if KNOWLEDGE_DIR.exists():
        return SimpleDirectoryReader(str(KNOWLEDGE_DIR)).load_data()
    return [Document(text="RAG 结合检索与生成。Agent 能调用工具完成任务。" * 5)]


def split_with_config(docs, chunk_size, chunk_overlap):
    """按配置切分并返回节点"""

    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = splitter.get_nodes_from_documents(docs)
    return nodes


def compare_splitters(docs):
    """对比不同切分参数"""

    configs = [
        (128, 20, "小块-高重叠"),
        (512, 50, "中块-标准"),
        (1024, 100, "大块-低重叠"),
    ]
    print("=== SentenceSplitter 对比 ===\n")
    for size, overlap, label in configs:
        nodes = split_with_config(docs, size, overlap)
        avg_len = sum(len(n.text) for n in nodes) / max(len(nodes), 1)
        print(f"[{label}] chunk_size={size}, overlap={overlap}")
        print(f"  节点数: {len(nodes)}, 平均长度: {avg_len:.0f} 字符")
        if nodes:
            print(f"  首节点预览: {nodes[0].text[:80]}...")
        print()


def show_node_metadata(nodes):
    """展示节点元数据"""

    print("=== 节点元数据示例 ===\n")
    for i, node in enumerate(nodes[:2], 1):
        print(f"节点 {i}: {node.metadata}")
        print(f"内容: {node.text[:100]}...\n")


if __name__ == "__main__":
    print("🚀 示例 2: LlamaIndex 文本切分\n")

    documents = load_sample_docs()
    print(f"加载文档数: {len(documents)}\n")
    compare_splitters(documents)
    nodes = split_with_config(documents, 512, 50)
    show_node_metadata(nodes)

    print("✅ 示例运行完成！")
