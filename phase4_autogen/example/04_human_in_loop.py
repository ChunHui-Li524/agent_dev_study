"""
==========================================
示例 4: AutoGen 人机协作
==========================================
学习目标：
1. 设置 human_input_mode="ALWAYS"
2. 在关键步骤由人工确认或补充
3. 理解 Human-in-the-Loop 工作流
"""

import os
from dotenv import load_dotenv
import autogen

load_dotenv()

CONFIG_LIST = [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]


def create_human_loop_agents():
    """创建需人工确认的 Agent"""

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.5},
        system_message="你是 AI 学习助手，回答准确简洁。",
    )
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="ALWAYS",
        max_consecutive_auto_reply=1,
        code_execution_config=False,
    )
    return assistant, user_proxy


def run_with_human_input():
    """运行一步需人工输入的对话"""

    assistant, user_proxy = create_human_loop_agents()
    print("=== 人机协作模式（ALWAYS）===\n")
    print("提示: 终端会提示输入，可直接回车使用默认回复，或输入自定义内容。\n")
    user_proxy.initiate_chat(
        assistant,
        message="请简要解释 LangChain 的 LCEL 是什么？",
    )


def run_second_turn_with_confirm():
    """第二轮继续需人工确认"""

    assistant, user_proxy = create_human_loop_agents()
    print("\n=== 第二轮追问（需人工确认）===\n")
    user_proxy.initiate_chat(
        assistant,
        message="请给一个 LCEL 链的简单代码示例思路。",
    )


if __name__ == "__main__":
    print("🚀 示例 4: AutoGen 人机协作\n")

    run_with_human_input()
    # run_second_turn_with_confirm()

    print("\n✅ 示例运行完成！")
