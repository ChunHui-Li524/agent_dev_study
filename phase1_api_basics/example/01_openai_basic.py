"""
==========================================
示例 1: OpenAI API 基础调用
==========================================
学习目标：
1. 如何使用 OpenAI SDK 调用 Chat Completion API
2. 理解核心参数：model、messages、temperature、max_tokens
3. 处理 API 响应
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    # 如果使用代理，取消下面的注释
    # base_url=os.getenv("OPENAI_BASE_URL")
)


def basic_completion():
    """最简单的调用示例"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 使用性价比最高的模型
        messages=[
            {"role": "system", "content": "你是一个有帮助的 AI 助手。"},
            {"role": "user", "content": "用简单的话解释什么是 AI Agent。"}
        ],
        temperature=0.7,    # 控制随机性：0 更确定，1 更随机
        max_tokens=500      # 限制输出长度
    )

    # 打印响应
    print("=== AI 回复 ===")
    print(response.choices[0].message.content)

    # 打印元信息
    print(f"\n=== 使用统计 ===")
    print(f"使用的模型: {response.model}")
    print(f"输入 Token 数: {response.usage.prompt_tokens}")
    print(f"输出 Token 数: {response.usage.completion_tokens}")
    print(f"总 Token 数: {response.usage.total_tokens}")


def multi_turn_conversation():
    """多轮对话示例（带上下文）"""

    conversation_history = [
        {"role": "system", "content": "你是一个专业的编程导师。"}
    ]

    # 第一轮对话
    conversation_history.append({
        "role": "user",
        "content": "什么是递归？"
    })

    response1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        temperature=0.7
    )

    answer1 = response1.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": answer1})

    print("=== 第一轮 ===")
    print(answer1)

    # 第二轮对话（会记住上一轮的内容）
    conversation_history.append({
        "role": "user",
        "content": "能给我一个递归的 Python 示例吗？"
    })

    response2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        temperature=0.7
    )

    answer2 = response2.choices[0].message.content

    print("\n=== 第二轮 ===")
    print(answer2)


def system_prompt_examples():
    """不同 System Prompt 的效果对比"""

    system_prompts = [
        "你是一个简洁的助手，用最少的字回答问题。",
        "你是一个详细的助手，尽可能完整地解释概念。",
        "你是一个幽默的助手，用轻松的语气回答。"
    ]

    question = "什么是机器学习？"

    for prompt in system_prompts:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7
        )

        print(f"\n=== System Prompt: {prompt} ===")
        print(response.choices[0].message.content)
        print("-" * 50)


if __name__ == "__main__":
    print("🚀 示例 1: OpenAI API 基础调用\n")

    # 运行各个示例
    # basic_completion()
    # multi_turn_conversation()
    system_prompt_examples()

    print("\n✅ 示例运行完成！")
