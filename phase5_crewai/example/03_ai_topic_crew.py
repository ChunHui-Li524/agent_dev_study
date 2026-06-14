"""
==========================================
示例 3: CrewAI AI 主题学习
==========================================
学习目标：
1. 垂直场景：本周学习 Function Calling
2. 多角色协作制定学习计划
3. 顺序执行 Task 产出学习方案
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

TOPIC = "Function Calling"


def build_topic_crew():
    """构建 Function Calling 主题 Crew"""

    planner = Agent(
        role="学习规划师",
        goal=f"为开发者制定 {TOPIC} 一周学习计划",
        backstory="你熟悉 LLM API 与工具调用最佳实践。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    coach = Agent(
        role="实战教练",
        goal="设计动手练习与自检清单",
        backstory="你注重学以致用，练习驱动学习。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    plan_task = Task(
        description=f"""
        主题: 本周学习 {TOPIC}
        输出: 5 天学习大纲（每天目标、推荐阅读、关键概念）
        """,
        expected_output="5 天 Function Calling 学习大纲。",
        agent=planner,
    )
    practice_task = Task(
        description="基于学习大纲，设计 3 个动手练习和自检问题。",
        expected_output="练习说明 + 自检清单。",
        agent=coach,
        context=[plan_task],
    )
    return Crew(
        agents=[planner, coach],
        tasks=[plan_task, practice_task],
        process=Process.sequential,
        verbose=True,
    )


if __name__ == "__main__":
    print("🚀 示例 3: CrewAI AI 主题学习\n")

    crew = build_topic_crew()
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print(result)

    print("\n✅ 示例运行完成！")
