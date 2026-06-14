"""
==========================================
示例 2: CrewAI 研究员 + 作家
==========================================
学习目标：
1. 顺序 Process 串联两个 Agent
2. 研究员调研 AI 主题，作家写科普
3. Task 上下文传递
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()


def build_researcher_writer_crew():
    """构建研究员-作家 Crew"""

    researcher = Agent(
        role="AI 技术研究员",
        goal="调研 AI Agent 技术要点并输出结构化笔记",
        backstory="你擅长从权威资料提炼技术要点。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    writer = Agent(
        role="科普作家",
        goal="将研究笔记写成通俗易懂的科普短文",
        backstory="你善于把复杂技术讲给初学者听。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    research_task = Task(
        description="调研 AI Agent：定义、能力、框架（LangChain/AutoGen/CrewAI）、应用。",
        expected_output="结构化调研笔记，含 4 个小节。",
        agent=researcher,
    )
    writing_task = Task(
        description="基于调研笔记，撰写 500 字左右的 AI Agent 科普文章。",
        expected_output="面向初学者的科普短文。",
        agent=writer,
        context=[research_task],
    )
    return Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )


if __name__ == "__main__":
    print("🚀 示例 2: CrewAI 研究员 + 作家\n")

    crew = build_researcher_writer_crew()
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("最终结果:")
    print(result)

    print("\n✅ 示例运行完成！")
