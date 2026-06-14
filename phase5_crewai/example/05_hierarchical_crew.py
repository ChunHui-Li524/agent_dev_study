"""
==========================================
示例 5: CrewAI 层级流程
==========================================
学习目标：
1. 使用 Process.hierarchical 层级执行
2. Manager 分配任务给下属 Agent
3. 结构化产出 AI 学习内容
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()


def build_hierarchical_crew():
    """构建层级 Crew"""

    researcher = Agent(
        role="调研员",
        goal="收集 AI RAG 技术资料",
        backstory="你负责资料收集。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    analyst = Agent(
        role="分析师",
        goal="分析资料并提炼洞察",
        backstory="你负责深度分析。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    writer = Agent(
        role="撰稿人",
        goal="撰写最终报告",
        backstory="你负责成稿输出。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    research_task = Task(
        description="收集 RAG 的定义、流程、优势。",
        expected_output="RAG 调研要点。",
        agent=researcher,
    )
    analysis_task = Task(
        description="分析调研要点，找出 3 个关键洞察。",
        expected_output="3 条洞察。",
        agent=analyst,
    )
    writing_task = Task(
        description="基于洞察撰写 300 字 RAG 入门介绍。",
        expected_output="RAG 入门介绍。",
        agent=writer,
    )
    return Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.hierarchical,
        manager_llm="gpt-4o-mini",
        verbose=True,
    )


if __name__ == "__main__":
    print("🚀 示例 5: CrewAI 层级流程\n")

    crew = build_hierarchical_crew()
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print(result)

    print("\n✅ 示例运行完成！")
