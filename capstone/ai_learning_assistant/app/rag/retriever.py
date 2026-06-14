"""RAG 检索器：LlamaIndex + ChromaDB（占位实现）。"""

from dataclasses import dataclass
from pathlib import Path

from app.core.config import load_config


@dataclass
class RetrievedChunk:
    """单条检索结果。"""

    text: str
    source_file: str
    score: float


class Retriever:
    """本地知识库检索器。

    TODO: 使用 LlamaIndex 构建索引，ChromaDB 持久化向量。
    """

    def __init__(self, knowledge_dir: Path | None = None) -> None:
        config = load_config()
        self._knowledge_dir = knowledge_dir or config.knowledge_dir
        self._index = None  # TODO: VectorStoreIndex

    def build_index(self) -> None:
        """从 knowledge_dir 加载文档并构建/更新索引。"""
        # TODO: SimpleDirectoryReader + VectorStoreIndex.from_documents
        raise NotImplementedError("build_index 尚未实现")

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        """检索与 query 最相关的文档片段。"""
        _ = query, top_k, self._knowledge_dir
        # TODO: query_engine 或 retriever.retrieve
        return []
