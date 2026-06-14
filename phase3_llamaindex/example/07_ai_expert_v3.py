"""
==========================================
示例 7: AI 专家 Agent v3（RAG + 对话）
==========================================
学习目标：
1. 结合 RAG 查询与多轮对话
2. 知识库无答案时诚实说明
3. LlamaIndex 版 AI 学习导师
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

SYSTEM_PROMPT = (
    "你是 AI 技术导师。优先基于检索到的知识回答；"
    "若上下文不足以回答，请明确说「根据当前知识库无法确定」，不要编造。"
)


def configure_settings():
    """配置 LLM 与 Embedding"""

    Settings.llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0.3,
    )
    Settings.embed_model = OpenAIEmbedding(api_key=os.getenv("OPENAI_API_KEY"))


def build_chat_engine():
    """构建 RAG + 对话 Chat Engine"""

    docs = SimpleDirectoryReader(str(KNOWLEDGE_DIR)).load_data()
    nodes = SentenceSplitter(chunk_size=512, chunk_overlap=50).get_nodes_from_documents(docs)
    index = VectorStoreIndex(nodes)
    return index.as_chat_engine(
        chat_mode="condense_question",
        similarity_top_k=3,
        system_prompt=SYSTEM_PROMPT,
        verbose=False,
    )


def run_chat_session(engine):
    """模拟多轮学习对话"""

    turns = [
        "什么是 RAG？",
        "它和我们刚学的 Agent 有什么关系？",
        "量子计算在 AI 中的最新突破是什么？",  # 知识库外问题
    ]
    for user_input in turns:
        print(f"用户: {user_input}")
        response = engine.chat(user_input)
        print(f"导师: {response}\n")


if __name__ == "__main__":
    print("🚀 示例 7: AI 专家 Agent v3\n")

    configure_settings()
    chat_engine = build_chat_engine()
    run_chat_session(chat_engine)

    print("✅ 示例运行完成！")
