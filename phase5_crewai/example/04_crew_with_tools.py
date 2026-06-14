"""
==========================================
示例 4: CrewAI 带工具
==========================================
学习目标：
1. 为 Agent 配置工具
2. 模拟本地 RAG 查询工具
3. Crew 执行中调用工具获取信息
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_core.tools import tool

load_dotenv()

MOCK_KB = {
    "RAG": "检索增强生成，结合向量检索与大模型。",
    "Agent": "能调用工具、多步推理的智能体。",
    "CrewAI": "多 Agent 角色协作框架。",
}


@tool
def mock_rag_search(query: str) -> str:
    """模拟本地知识库检索，输入查询关键词。"""

    for key, value in MOCK_KB.items():
        if key.lower() in query.lower():
            return f"[{key}] {value}"
    return "知识库未找到相关内容。"


def build_crew_with_tools():
    """构建带工具的 Crew"""

    researcher = Agent(
        role="知识检索员",
        goal="使用工具检索 AI 概念并汇总",
        backstory="你依赖本地知识库回答问题。",
        tools=[mock_rag_search],
        verbose=True,
        llm="gpt-4o-mini",
    )
    summarizer = Agent(
        role="摘要员",
        goal="将检索结果整理成学习卡片",
        backstory="你擅长提炼要点。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    search_task = Task(
        description="使用工具检索 RAG 和 Agent 的定义，汇总要点。",
        expected_output="两个概念的定义摘要。",
        agent=researcher,
    )
    summary_task = Task(
        description="将检索摘要整理为 3 条学习卡片。",
        expected_output="3 条学习卡片。",
        agent=summarizer,
        context=[search_task],
    )
    return Crew(
        agents=[researcher, summarizer],
        tasks=[search_task, summary_task],
        process=Process.sequential,
        verbose=True,
    )


if __name__ == "__main__":
    print("🚀 示例 4: CrewAI 带工具\n")

    crew = build_crew_with_tools()
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print(result)

    print("\n✅ 示例运行完成！")
