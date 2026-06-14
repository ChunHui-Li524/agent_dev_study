"""
==========================================
示例 3: 错误处理与重试
==========================================
学习目标：
1. 捕获 API 超时、限流等常见错误
2. 实现指数退避重试
3. 封装可复用的 call_llm() 函数

practice 改用通义千问：
  client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                  base_url=os.getenv("DASHSCOPE_BASE_URL"))
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI, APITimeoutError, RateLimitError, APIConnectionError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AI_EXPERT_SYSTEM = (
    "你是 AI 技术导师，用简洁准确的语言解答 LLM、Agent、RAG 等相关问题。"
)


def call_llm(messages, model="gpt-4o-mini", max_retries=3, timeout=30):
    """带重试的 LLM 调用封装"""

    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                timeout=timeout,
            )
        except RateLimitError:
            wait = 2 ** attempt
            print(f"限流，{wait}s 后重试 ({attempt + 1}/{max_retries})")
            time.sleep(wait)
        except (APITimeoutError, APIConnectionError) as err:
            wait = 2 ** attempt
            print(f"网络/超时: {err}，{wait}s 后重试")
            time.sleep(wait)

    raise RuntimeError(f"重试 {max_retries} 次后仍失败")


def demo_basic_retry():
    """基础重试示例"""

    messages = [
        {"role": "system", "content": AI_EXPERT_SYSTEM},
        {"role": "user", "content": "用一句话解释什么是 Function Calling。"},
    ]
    response = call_llm(messages)
    print(response.choices[0].message.content)


def demo_invalid_key_hint():
    """说明常见认证错误（不主动触发）"""

    print("常见错误排查：")
    print("  - 401: API Key 无效或未配置 .env")
    print("  - 429: 请求过于频繁，使用指数退避")
    print("  - timeout: 增大 timeout 或检查网络/代理")


if __name__ == "__main__":
    print("🚀 示例 3: 错误处理与重试\n")
    demo_basic_retry()
    print()
    demo_invalid_key_hint()
    print("\n✅ 示例运行完成！")
