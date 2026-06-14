"""
==========================================
示例 6: LlamaIndex RAG 简易评测
==========================================
学习目标：
1. 构建小型评测问答集
2. 循环提问并记录回答
3. 简单关键词命中率评估
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

EVAL_SET = [
    {"question": "什么是 RAG？", "keywords": ["检索", "生成"]},
    {"question": "AI Agent 的核心能力有哪些？", "keywords": ["规划", "工具"]},
    {"question": "Function Calling 如何工作？", "keywords": ["工具", "JSON"]},
    {"question": "RAG 的优势是什么？", "keywords": ["幻觉", "知识"]},
    {"question": "Agent 常见框架有哪些？", "keywords": ["LangChain", "AutoGen"]},
]


def configure_settings():
    """配置模型"""

    Settings.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    Settings.embed_model = OpenAIEmbedding(api_key=os.getenv("OPENAI_API_KEY"))


def build_engine():
    """构建查询引擎"""

    docs = SimpleDirectoryReader(str(KNOWLEDGE_DIR)).load_data()
    nodes = SentenceSplitter(chunk_size=512, chunk_overlap=50).get_nodes_from_documents(docs)
    return VectorStoreIndex(nodes).as_query_engine(similarity_top_k=3)


def score_answer(answer, keywords):
    """关键词命中率评分"""

    hits = sum(1 for kw in keywords if kw in answer)
    return hits / len(keywords)


def run_eval_loop(engine):
    """运行评测循环"""

    print("=== RAG 简易评测 ===\n")
    scores = []
    for i, item in enumerate(EVAL_SET, 1):
        response = str(engine.query(item["question"]))
        score = score_answer(response, item["keywords"])
        scores.append(score)
        print(f"Q{i}: {item['question']}")
        print(f"  关键词命中: {score:.0%}")
        print(f"  回答摘要: {response[:100]}...\n")
    avg = sum(scores) / len(scores)
    print(f"平均关键词命中率: {avg:.0%}")


if __name__ == "__main__":
    print("🚀 示例 6: LlamaIndex RAG 简易评测\n")

    configure_settings()
    query_engine = build_engine()
    run_eval_loop(query_engine)

    print("\n✅ 示例运行完成！")
