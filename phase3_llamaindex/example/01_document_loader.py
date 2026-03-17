"""
==========================================
示例 1: LlamaIndex Document Loaders
==========================================
学习目标：
1. 使用 SimpleDirectoryReader 加载本地文件
2. 从不同数据源加载文档（网页、数据库）
3. 理解 Document 对象结构
"""

import os
from dotenv import load_dotenv
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader

load_dotenv()


def load_local_files():
    """加载本地文件"""

    # 假设有一个 data 文件夹
    # 如果文件夹不存在，使用示例文档
    if not os.path.exists("data"):
        print("注意：未找到 data 文件夹，使用示例文档\n")

        # 创建示例文档
        documents = [
            Document(text="AI Agent 是一个能够自主感知、推理和行动的智能系统。"),
            Document(text="LangChain 是一个开发框架，用于构建 LLM 应用。"),
            Document(text="LlamaIndex 专注于数据索引和检索增强生成（RAG）。")
        ]

        print("=== 示例文档 ===")
        for i, doc in enumerate(documents, 1):
            print(f"\n文档 {i}:")
            print(f"内容: {doc.text}")
            print(f"元数据: {doc.metadata}")
    else:
        # 从文件夹加载所有文件
        reader = SimpleDirectoryReader("data")
        documents = reader.load_data()

        print(f"=== 加载了 {len(documents)} 个文档 ===\n")

        for i, doc in enumerate(documents, 1):
            print(f"文档 {i}:")
            print(f"内容预览: {doc.text[:100]}...")
            print(f"元数据: {doc.metadata}\n")

    return documents


def load_specific_files():
    """加载特定文件"""

    # 可以指定加载的文件类型
    reader = SimpleDirectoryReader(
        input_files=["data/document1.txt", "data/document2.pdf"]
    )

    documents = reader.load_data()

    print(f"=== 加载了 {len(documents)} 个特定文件 ===")
    for doc in documents:
        print(f"- {doc.metadata.get('file_name', '未知')}")

    return documents


def load_web_page():
    """加载网页内容"""

    urls = [
        "https://www.example.com",
        "https://python.org"
    ]

    try:
        documents = SimpleWebPageReader(html_to_text=True).load_data(urls)

        print(f"=== 加载了 {len(documents)} 个网页 ===\n")

        for i, doc in enumerate(documents, 1):
            print(f"网页 {i}:")
            print(f"URL: {doc.metadata.get('source', '未知')}")
            print(f"内容预览: {doc.text[:200]}...\n")

        return documents

    except Exception as e:
        print(f"加载网页时出错: {e}")
        return []


def create_custom_documents():
    """创建自定义文档（带元数据）"""

    documents = [
        Document(
            text="AI Agent 是人工智能代理，能够感知环境、做出决策并执行行动。",
            metadata={
                "source": "自定义文档",
                "category": "定义",
                "author": "AI 学习者"
            }
        ),
        Document(
            text="LangChain 提供了 Chain、Agent、Memory 等核心组件。",
            metadata={
                "source": "自定义文档",
                "category": "框架",
                "author": "AI 学习者"
            }
        )
    ]

    print("=== 自定义文档 ===")
    for doc in documents:
        print(f"\n内容: {doc.text}")
        print(f"元数据: {doc.metadata}")

    return documents


def document_operations():
    """文档操作示例"""

    documents = create_custom_documents()

    print("\n=== 文档操作 ===\n")

    # 合并文档
    merged_doc = Document(text="\n\n".join([d.text for d in documents]))
    print(f"合并后的文档长度: {len(merged_doc.text)} 字符")

    # 提取元数据
    categories = [d.metadata.get("category") for d in documents]
    print(f"所有类别: {categories}")

    # 过滤文档
    definition_docs = [d for d in documents if d.metadata.get("category") == "定义"]
    print(f"定义类文档数: {len(definition_docs)}")


if __name__ == "__main__":
    print("🚀 示例 1: LlamaIndex Document Loaders\n")

    # 运行各个示例
    load_local_files()
    # load_specific_files()
    # load_web_page()
    # create_custom_documents()
    # document_operations()

    print("\n✅ 示例运行完成！")
