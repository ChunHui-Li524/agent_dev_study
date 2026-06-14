"""
==========================================
示例 6: CrewAI AI 内容流水线
==========================================
学习目标：
1. 端到端：主题 -> FAQ + 学习路径
2. 多 Agent 分工协作
3. 产出可直接使用的学习材料
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

TOPIC = "AI Agent"


def build_content_pipeline():
    """构建内容流水线 Crew"""

    strategist = Agent(
        role="学习策略师",
        goal=f"为 {TOPIC} 设计学习路径",
        backstory="你擅长规划循序渐进的学习路线。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    faq_writer = Agent(
        role="FAQ 撰写员",
        goal="编写常见问题解答",
        backstory="你善于预判初学者疑问。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    reviewer = Agent(
        role="内容审稿人",
        goal="整合并润色最终交付物",
        backstory="你确保内容准确、结构清晰。",
        verbose=True,
        llm="gpt-4o-mini",
    )
    path_task = Task(
        description=f"为主题「{TOPIC}」设计 4 步学习路径，每步含目标与预计时间。",
        expected_output="4 步学习路径。",
        agent=strategist,
    )
    faq_task = Task(
        description=f"为主题「{TOPIC}」编写 5 个 FAQ（问+答）。",
        expected_output="5 个 FAQ。",
        agent=faq_writer,
    )
    review_task = Task(
        description="整合学习路径与 FAQ，输出最终学习包（路径+FAQ）。",
        expected_output="完整学习包：学习路径 + FAQ。",
        agent=reviewer,
        context=[path_task, faq_task],
    )
    return Crew(
        agents=[strategist, faq_writer, reviewer],
        tasks=[path_task, faq_task, review_task],
        process=Process.sequential,
        verbose=True,
    )


if __name__ == "__main__":
    print("🚀 示例 6: CrewAI AI 内容流水线\n")

    crew = build_content_pipeline()
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("学习包输出:")
    print(result)

    print("\n✅ 示例运行完成！")
