"""
==========================================
示例 6: LangChain ReAct Agent
==========================================
学习目标：
1. 使用 create_react_agent 创建 Agent
2. Agent 自动选择并调用工具
3. 构建 AI 专家问答 Agent
"""

import os
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

GLOSSARY = {
    "RAG": "检索增强生成：结合检索与生成。",
    "ReAct": "Reasoning + Acting：推理与行动交替的 Agent 模式。",
}


@tool
def lookup_glossary(term: str) -> str:
    """查询 AI 术语定义。"""

    return GLOSSARY.get(term, f"未找到: {term}")


@tool
def recommend_topic(interest: str) -> str:
    """根据兴趣推荐学习主题。"""

    mapping = {"RAG": "Phase 3", "Agent": "Phase 4", "Crew": "Phase 5"}
    for key, phase in mapping.items():
        if key.lower() in interest.lower():
            return f"推荐学习 {key}，参见 {phase}"
    return "建议从 Phase 1 API 基础开始。"


def build_react_agent():
    """创建 ReAct Agent 执行器"""

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0,
    )
    tools = [lookup_glossary, recommend_topic]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)


def run_agent_questions(executor):
    """运行示例问题"""

    questions = [
        "RAG 是什么？查一下术语并简要说明。",
    ]
    for q in questions:
        print(f"\n=== 问题: {q} ===\n")
        result = executor.invoke({"input": q})
        print(f"\n回答: {result['output']}\n")


if __name__ == "__main__":
    print("🚀 示例 6: LangChain ReAct Agent\n")

    agent_executor = build_react_agent()
    run_agent_questions(agent_executor)

    print("✅ 示例运行完成！")
