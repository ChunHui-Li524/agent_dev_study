"""
==========================================
示例 1: AutoGen 基础对话
==========================================
学习目标：
1. 创建 Assistant Agent 和 User Proxy Agent
2. 发起对话并观察交互
3. 理解对话终止条件
"""

import os
from dotenv import load_dotenv
import autogen

load_dotenv()

# 配置 LLM
config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

# 创建 Assistant Agent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0.7,
    },
    system_message="你是一个有帮助的 AI 助手，能够回答各种问题。",
)

# 创建 User Proxy Agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # 自动执行，不请求人工输入
    max_consecutive_auto_reply=10,  # 最多自动回复次数
    code_execution_config=False,  # 不执行代码
)

print("🚀 AutoGen 基础对话示例\n")
print("=" * 60)


def basic_conversation():
    """基础对话示例"""

    print("\n=== 示例 1: 简单问答 ===\n")

    # 发起对话
    response = user_proxy.initiate_chat(
        assistant,
        message="你好！请用简单的话解释什么是 AI Agent。",
    )

    print("\n对话结束。")


def multi_turn_conversation():
    """多轮对话示例"""

    print("\n=== 示例 2: 多轮对话 ===\n")

    # 连续发起多个问题
    questions = [
        "什么是机器学习？",
        "机器学习和深度学习有什么区别？",
        "能给我一个深度学习的实际应用例子吗？"
    ]

    for question in questions:
        print(f"用户: {question}")
        user_proxy.initiate_chat(
            assistant,
            message=question,
        )
        print("\n" + "-" * 50 + "\n")


def conversation_with_clearance():
    """带有终止条件的对话"""

    print("\n=== 示例 3: 自定义终止条件 ===\n")

    # 创建带有自定义终止条件的 User Proxy
    user_proxy_custom = autogen.UserProxyAgent(
        name="user_proxy_custom",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,  # 限制自动回复次数
        code_execution_config=False,
    )

    user_proxy_custom.initiate_chat(
        assistant,
        message="请详细介绍 Python 的装饰器，包括其原理和使用场景。"
    )


def conversation_with_summary():
    """带摘要的对话"""

    print("\n=== 示例 4: 保存对话历史 ===\n")

    # 创建一个助手，用于总结
    summarizer = autogen.AssistantAgent(
        name="summarizer",
        llm_config={
            "config_list": config_list,
            "temperature": 0.5,
        },
        system_message="你是一个总结专家，能够简洁地总结对话内容。",
    )

    # 先进行对话
    print("进行对话...\n")
    user_proxy.initiate_chat(
        assistant,
        message="给我介绍一下 LangChain 框架。",
    )

    # 总结对话
    print("\n=== 对话总结 ===\n")
    # 注意：这里需要访问实际的对话历史
    # 在实际应用中，可以从 agent.chat_messages 获取


if __name__ == "__main__":
    # 运行各个示例
    # basic_conversation()
    # multi_turn_conversation()
    conversation_with_clearance()
    # conversation_with_summary()

    print("\n✅ 示例运行完成！")
