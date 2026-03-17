"""
==========================================
示例 1: CrewAI 基础概念
==========================================
学习目标：
1. 理解 Agent、Task、Crew 三大核心概念
2. 创建简单的 Agent 和 Task
3. 组装并执行 Crew
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()


def basic_example():
    """最基础的 CrewAI 示例"""

    print("🚀 CrewAI 基础示例\n")
    print("=" * 60)

    # 步骤 1: 创建 Agent
    researcher = Agent(
        role="高级研究员",
        goal="研究和分析最新技术趋势",
        backstory="你是一名经验丰富的研究员，擅长深入分析和总结技术发展。",
        verbose=True,
        llm="gpt-4o-mini"  # 可以直接指定模型
    )

    writer = Agent(
        role="技术作家",
        goal="将研究成果转化为通俗易懂的文章",
        backstory="你是一名优秀的技术作家，擅长将复杂技术解释清楚。",
        verbose=True,
        llm="gpt-4o-mini"
    )

    # 步骤 2: 创建 Task
    research_task = Task(
        description="""
        研究 AI Agent 技术的最新发展趋势。
        需要涵盖：
        1. 主要技术框架（LangChain、AutoGen、CrewAI）
        2. 应用场景和案例
        3. 未来发展方向
        """,
        expected_output="一份详细的研究报告，包含技术框架、应用案例和未来趋势分析。",
        agent=researcher
    )

    writing_task = Task(
        description="""
        基于研究报告，撰写一篇面向初学者的 AI Agent 技术文章。
        要求：
        1. 语言通俗易懂
        2. 结构清晰（引言、主体、总结）
        3. 包含实际应用案例
        4. 字数控制在 1500 字左右
        """,
        expected_output="一篇完整的技术文章，适合初学者阅读。",
        agent=writer
    )

    # 步骤 3: 创建 Crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,  # 顺序执行
        verbose=True
    )

    # 步骤 4: 执行 Crew
    print("\n开始执行任务...\n")
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("任务完成！\n")
    print("最终结果：")
    print(result)


def minimal_example():
    """最简示例 - 快速上手"""

    print("\n🚀 最简示例\n")
    print("=" * 60)

    # 一个 Agent，一个 Task
    agent = Agent(
        role="AI 助手",
        goal="回答用户问题",
        backstory="你是一个有帮助的 AI 助手。",
        verbose=False,
        llm="gpt-4o-mini"
    )

    task = Task(
        description="用简单的话解释什么是 AI Agent。",
        expected_output="一段简短的 AI Agent 解释。",
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("结果：")
    print(result)


def example_with_context():
    """带上下文传递的示例"""

    print("\n🚀 带上下文的示例\n")
    print("=" * 60)

    # Agent 1: 分析师
    analyst = Agent(
        role="数据分析师",
        goal="分析数据并提取关键信息",
        backstory="你是一名专业数据分析师，擅长从复杂数据中发现规律。",
        verbose=True,
        llm="gpt-4o-mini"
    )

    # Agent 2: 策略师
    strategist = Agent(
        role="商业策略师",
        goal="基于分析结果制定策略",
        backstory="你是一名资深商业策略师，擅长将分析转化为可执行的策略。",
        verbose=True,
        llm="gpt-4o-mini"
    )

    # Task 1: 数据分析
    analysis_task = Task(
        description="""
        分析以下销售数据：
        - Q1: 100万
        - Q2: 120万
        - Q3: 150万
        - Q4: 180万

        找出趋势和关键增长点。
        """,
        expected_output="销售数据分析报告，包含趋势分析。",
        agent=analyst
    )

    # Task 2: 策略制定（依赖 Task 1 的结果）
    strategy_task = Task(
        description="""
        基于销售数据分析结果，制定下一年度的销售策略。
        需要包含：
        1. 目标销售额
        2. 关键举措
        3. 资源分配建议
        """,
        expected_output="详细的销售策略方案。",
        agent=strategist,
        context=[analysis_task]  # 传递上下文
    )

    crew = Crew(
        agents=[analyst, strategist],
        tasks=[analysis_task, strategy_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("最终策略：")
    print(result)


if __name__ == "__main__":
    # 运行各个示例
    # minimal_example()
    # basic_example()
    example_with_context()

    print("\n✅ 示例运行完成！")
