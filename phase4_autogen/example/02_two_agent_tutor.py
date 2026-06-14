"""
==========================================
示例 2: AutoGen 双 Agent 导师-学员
==========================================
学习目标：
1. 创建 Tutor 和 Learner 两个 Assistant
2. 由 UserProxy 引导双方讨论
3. 模拟 AI 概念研讨对话
"""

import os
from dotenv import load_dotenv
import autogen

load_dotenv()

CONFIG_LIST = [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]


def create_agents():
    """创建导师、学员与协调者"""

    tutor = autogen.AssistantAgent(
        name="tutor",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.5},
        system_message="你是 AI 导师，用清晰例子讲解 Agent 概念，每次回复不超过 150 字。",
    )
    learner = autogen.AssistantAgent(
        name="learner",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.7},
        system_message="你是积极的学习者，会提问、总结并追问，每次回复不超过 100 字。",
    )
    coordinator = autogen.UserProxyAgent(
        name="coordinator",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=6,
        code_execution_config=False,
    )
    return tutor, learner, coordinator


def tutor_learner_discussion():
    """导师与学员讨论 Agent"""

    tutor, learner, coordinator = create_agents()
    groupchat = autogen.GroupChat(
        agents=[tutor, learner],
        messages=[],
        max_round=4,
        speaker_selection_method="round_robin",
    )
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={"config_list": CONFIG_LIST},
    )

    print("=== 导师 + 学员讨论: 什么是 Agent ===\n")
    coordinator.initiate_chat(
        manager,
        message="请一起讨论：什么是 AI Agent？导师先讲解，学员提问和总结。",
    )


if __name__ == "__main__":
    print("🚀 示例 2: AutoGen 双 Agent 导师-学员\n")

    tutor_learner_discussion()

    print("\n✅ 示例运行完成！")
