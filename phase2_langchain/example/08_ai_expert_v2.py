"""
==========================================
示例 8: AI 专家 Agent v2（LangChain 综合）
==========================================
学习目标：
1. 组合 Memory + Agent + 工具
2. LangChain 版 AI 学习导师
3. 多轮对话中查术语并推荐主题
"""

import os
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

GLOSSARY = {
    "RAG": "检索增强生成：先检索知识库再生成。",
    "Agent": "能感知、规划、调用工具的智能体。",
    "LCEL": "LangChain Expression Language，用 | 组合组件。",
}


@tool
def lookup_glossary(term: str) -> str:
    """查询 AI 术语定义。"""

    return GLOSSARY.get(term, f"未找到: {term}")


@tool
def recommend_topic(phase: str) -> str:
    """根据当前学习阶段推荐下一步，如 Phase1/Phase2。"""

    roadmap = {
        "Phase1": "继续学 Function Calling 与流式 Tool",
        "Phase2": "学习 ReAct Agent 与 LangChain RAG",
        "Phase3": "学习 LlamaIndex 向量索引与引用",
    }
    return roadmap.get(phase, "建议从 Phase1 API 基础开始。")


def build_ai_expert_v2():
    """构建带记忆的 AI 专家 Agent"""

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0.3,
    )
    tools = [lookup_glossary, recommend_topic]
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=4,
        handle_parsing_errors=True,
    )
    return executor


def run_learning_session(executor):
    """模拟学习会话"""

    turns = [
        "我在学 Phase2，请查一下 RAG 的定义。",
        "根据我当前阶段，推荐下一步学什么？",
    ]
    for user_input in turns:
        print(f"\n用户: {user_input}\n")
        result = executor.invoke({"input": user_input})
        print(f"专家: {result['output']}\n")


if __name__ == "__main__":
    print("🚀 示例 8: AI 专家 Agent v2\n")

    expert = build_ai_expert_v2()
    run_learning_session(expert)

    print("✅ 示例运行完成！")
