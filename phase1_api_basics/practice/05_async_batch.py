"""
练习 05: 异步批量
对应 example: example/05_async_batch.py
学习目标: AsyncOpenAI 并发
完成日期:2026/06/14
自检: [√] 闭卷重写  [√] 变式完成  [√] 运行通过

变式要求（AI 专家 Agent）: 批量问 3 个 AI 概念
"""
import os

import asyncio
from dotenv import load_dotenv
from openai import AsyncClient, APITimeoutError, APIStatusError

load_dotenv()


async def batch_ask_questions():
    async_client = AsyncClient(
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    questions = get_questions()
    tasks = [ask_question(async_client, question) for question in questions]
    result = await asyncio.gather(*tasks)
    for question, answer in result:
        print("-"*20)
        print(f"【User】: {question}")
        print(f"【AI】: {answer}")


def get_questions():
    return [
        "解释一下prompt",
        "解释一下RAG",
        "解释一下Agent",
    ]


async def ask_question(client: AsyncClient, question: str):
    print(f"开始等待AI回答：{question}")
    messages = [
        {"role": "system", "content": "你是一个AI专家，用精简的话回答用户的提问"},
        {"role": "user", "content": question},
    ]

    try:
        response = await client.chat.completions.create(
            messages=messages,
            model="qwen3.6-27b",
            temperature=0.8,
            stream=False
        )
    except APITimeoutError as e:
        answer = f"API超时：{e}"
    except APIStatusError as e:
        answer = f"API接口对接错误：{e}"
    except Exception as e:
        answer = f"AI访问异常：{e}"
    else:
        if response.choices:
            if response.choices[0].message.content:
                answer = response.choices[0].message.content
            else:
                answer = "No Response"
        else:
            answer = "AI Error: No Choice"
    return question, answer


if __name__ == "__main__":
    asyncio.run(batch_ask_questions())

# ============================================================
# 评卷意见（AI课程评卷老师 | 2026-06-14）
# 结论: 通过 ✅  |  得分: 95/100
# 运行验证: PyCharm 运行通过（exit code 0，3 题并发请求）
# ------------------------------------------------------------
# 优点:
#   - AsyncClient + asyncio.gather 并发逻辑正确
#   - 批量问 prompt/RAG/Agent 三个 AI 概念，变式完成
#   - 函数职责分离清晰，失败时返回可读错误信息
#   - 「开始等待AI回答」先于结果输出，证明并发发起
# 待改进:
#   1. except Exception 可收窄为 OpenAIError 等 SDK 异常
#   2. 可用 async with AsyncClient(...) 自动关闭连接
#   3. （可选）加并发 vs 顺序耗时对比
# 检查项:
#   [√] AsyncClient 异步调用
#   [√] asyncio.gather 并发
#   [√] 批量 3 个 AI 概念
#   [√] AI 专家 persona
#   [√] 通义千问环境变量
#   [√] 可独立运行
# ============================================================
