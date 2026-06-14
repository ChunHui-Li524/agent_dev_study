"""
==========================================
示例 5: 异步并发批量请求
==========================================
学习目标：
1. 使用 AsyncOpenAI 并发调用
2. 批量提问多个 AI 概念并汇总
"""

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

QUESTIONS = [
    "用一句话解释什么是 LLM。",
    "用一句话解释什么是 RAG。",
    "用一句话解释什么是 Agent。",
]


async def ask_one(question):
    """异步单次提问"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是 AI 技术导师，回答极简。"},
            {"role": "user", "content": question},
        ],
    )
    return question, response.choices[0].message.content


async def batch_ask(questions):
    """并发提问"""

    tasks = [ask_one(q) for q in questions]
    return await asyncio.gather(*tasks)


async def sequential_ask(questions):
    """顺序提问（对比用）"""

    results = []
    for q in questions:
        results.append(await ask_one(q))
    return results


async def main():
    print("=== 并发批量提问 ===\n")
    results = await batch_ask(QUESTIONS)
    for question, answer in results:
        print(f"Q: {question}")
        print(f"A: {answer}\n")


if __name__ == "__main__":
    print("🚀 示例 5: 异步批量请求\n")
    asyncio.run(main())
    print("✅ 示例运行完成！")
