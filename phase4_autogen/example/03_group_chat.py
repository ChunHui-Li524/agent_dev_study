"""
==========================================
示例 3: AutoGen Group Chat
==========================================
学习目标：
1. 创建 3 个 Agent 群组对话
2. 使用 GroupChat 与 GroupChatManager
3. 导师、练习者、审查者协作学习
"""

import os
from dotenv import load_dotenv
import autogen

load_dotenv()

CONFIG_LIST = [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]


def build_study_group():
    """构建学习小组 Agent"""

    tutor = autogen.AssistantAgent(
        name="tutor",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.4},
        system_message="AI 导师：讲解概念，回复简洁。",
    )
    practicer = autogen.AssistantAgent(
        name="practicer",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.6},
        system_message="练习者：用例子巩固理解，提出实践问题。",
    )
    reviewer = autogen.AssistantAgent(
        name="reviewer",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.3},
        system_message="审查者：检查讲解是否准确，指出遗漏。",
    )
    user = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )
    return [user, tutor, practicer, reviewer]


def run_group_chat(agents, topic):
    """运行群组讨论"""

    user, tutor, practicer, reviewer = agents
    groupchat = autogen.GroupChat(
        agents=[tutor, practicer, reviewer],
        messages=[],
        max_round=6,
        speaker_selection_method="round_robin",
    )
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={"config_list": CONFIG_LIST},
    )
    print(f"=== 群组讨论: {topic} ===\n")
    user.initiate_chat(manager, message=f"请大家讨论：{topic}")


if __name__ == "__main__":
    print("🚀 示例 3: AutoGen Group Chat\n")

    agents = build_study_group()
    run_group_chat(agents, "什么是 RAG，它解决了什么问题？")

    print("\n✅ 示例运行完成！")
