"""
==========================================
示例 6: AutoGen AI 学习小组报告
==========================================
学习目标：
1. 多 Agent 协作产出学习报告
2. 研究员、作家、审稿人分工
3. 综合 AutoGen 多 Agent 能力
"""

import os
from dotenv import load_dotenv
import autogen

load_dotenv()

CONFIG_LIST = [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]


def build_study_panel():
    """构建学习小组 Agent"""

    researcher = autogen.AssistantAgent(
        name="researcher",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.4},
        system_message="研究员：收集 AI Agent 核心概念要点，条理清晰。",
    )
    writer = autogen.AssistantAgent(
        name="writer",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.6},
        system_message="作家：将要点写成初学者友好的学习报告，约 300 字。",
    )
    editor = autogen.AssistantAgent(
        name="editor",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.3},
        system_message="审稿人：检查报告准确性，输出最终版。",
    )
    coordinator = autogen.UserProxyAgent(
        name="coordinator",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=8,
        code_execution_config=False,
    )
    return researcher, writer, editor, coordinator


def run_study_report_pipeline():
    """流水线：研究 -> 写作 -> 审稿"""

    researcher, writer, editor, coordinator = build_study_panel()
    topic = "AI Agent 技术学习报告"

    print(f"=== {topic} ===\n")

    coordinator.initiate_chat(
        researcher,
        message="请列出 AI Agent 的定义、关键能力、主流框架、学习路径四个要点。",
    )
    coordinator.initiate_chat(
        writer,
        message="请根据研究员的要点，撰写初学者学习报告。",
    )
    coordinator.initiate_chat(
        editor,
        message="请审稿并输出最终学习报告。",
    )


if __name__ == "__main__":
    print("🚀 示例 6: AutoGen AI 学习小组报告\n")

    run_study_report_pipeline()

    print("\n✅ 示例运行完成！")
