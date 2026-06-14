"""
==========================================
示例 4: LangChain Memory
==========================================
学习目标：
1. 使用 ConversationBufferMemory 保存对话历史
2. 结合 LLM 实现带记忆的 AI 导师
3. 多轮对话中记住用户学习进度
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0.7,
)


def build_memory_chain():
    """构建带记忆的对话链"""

    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是 AI 学习导师，记住用户正在学习的阶段和内容。"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
    ])
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=False)
    return chain, memory


def chat_session(chain):
    """模拟多轮学习对话"""

    turns = [
        "我正在学习 Phase 2 LangChain，刚学完 Prompt Template。",
        "我当前学到哪个阶段了？",
        "接下来应该学什么？",
    ]
    for user_input in turns:
        print(f"用户: {user_input}")
        response = chain.invoke({"input": user_input})
        print(f"导师: {response['text']}\n")


def show_memory(memory):
    """展示记忆中的对话历史"""

    print("=== 对话记忆 ===\n")
    messages = memory.chat_memory.messages
    for msg in messages:
        role = "用户" if msg.type == "human" else "导师"
        print(f"{role}: {msg.content[:120]}...")
    print()


if __name__ == "__main__":
    print("🚀 示例 4: LangChain Memory\n")

    memory_chain, mem = build_memory_chain()
    chat_session(memory_chain)
    show_memory(mem)

    print("✅ 示例运行完成！")
