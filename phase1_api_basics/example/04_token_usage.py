"""
==========================================
示例 4: Token 使用量与成本估算
==========================================
学习目标：
1. 读取 response.usage 字段
2. 估算单次对话成本
3. 在 AI 专家场景中记录 token 消耗
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 单价示例（美元/1M tokens，仅供参考，以官方为准）
PRICE_PER_1M = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}


def estimate_cost(model, prompt_tokens, completion_tokens):
    """估算单次调用成本（美元）"""

    rates = PRICE_PER_1M.get(model, {"input": 0, "output": 0})
    input_cost = prompt_tokens / 1_000_000 * rates["input"]
    output_cost = completion_tokens / 1_000_000 * rates["output"]
    return input_cost + output_cost


def ask_with_usage(question):
    """提问并打印 token 统计"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是 AI 技术导师。"},
            {"role": "user", "content": question},
        ],
    )

    usage = response.usage
    cost = estimate_cost(
        response.model,
        usage.prompt_tokens,
        usage.completion_tokens,
    )

    print(f"问题: {question}")
    print(f"回答: {response.choices[0].message.content[:200]}...")
    print(f"\n--- Token 统计 ---")
    print(f"输入: {usage.prompt_tokens}")
    print(f"输出: {usage.completion_tokens}")
    print(f"合计: {usage.total_tokens}")
    print(f"估算成本: ${cost:.6f}")


def session_tracker():
    """模拟多轮对话累计 token"""

    total_tokens = 0
    questions = [
        "什么是 RAG？",
        "RAG 和微调有什么区别？",
    ]

    messages = [{"role": "system", "content": "你是 AI 技术导师。"}]

    for q in questions:
        messages.append({"role": "user", "content": q})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        answer = response.choices[0].message.content
        messages.append({"role": "assistant", "content": answer})
        total_tokens += response.usage.total_tokens
        print(f"[{q}] tokens={response.usage.total_tokens}")

    print(f"\n会话累计 tokens: {total_tokens}")


if __name__ == "__main__":
    print("🚀 示例 4: Token 使用量\n")
    ask_with_usage("解释什么是 Agent？")
    print("\n" + "=" * 50 + "\n")
    session_tracker()
    print("\n✅ 示例运行完成！")
