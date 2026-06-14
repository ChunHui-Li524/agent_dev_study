"""
==========================================
示例 9: AI 专家 Agent v1（Phase 1 综合）
==========================================
学习目标：
1. 串联流式对话 + Tool + 重试 + Token 日志
2. CLI 交互式 AI 学习助手原型
"""

import json
import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APITimeoutError, APIConnectionError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AI_EXPERT_SYSTEM = (
    "你是 AI 技术导师，帮助开发者理解 LLM、Agent、RAG、Prompt 等概念。"
    "回答准确、结构化，必要时使用工具查询术语。"
)

GLOSSARY = {
    "RAG": "检索增强生成：先检索知识库再生成回答。",
    "Agent": "能调用工具、多步推理完成目标的 LLM 应用。",
    "Function Calling": "模型结构化输出工具调用请求的能力。",
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_glossary",
            "description": "查询 AI 术语定义",
            "parameters": {
                "type": "object",
                "properties": {"term": {"type": "string"}},
                "required": ["term"],
            },
        },
    }
]

SESSION_TOKENS = 0


def call_llm(messages, stream=False, max_retries=3):
    """带重试的调用"""

    global SESSION_TOKENS
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOLS,
                stream=stream,
                timeout=30,
            )
            if not stream and response.usage:
                SESSION_TOKENS += response.usage.total_tokens
            return response
        except (RateLimitError, APITimeoutError, APIConnectionError):
            time.sleep(2 ** attempt)
    raise RuntimeError("API 调用失败")


def handle_tool_calls(message, messages):
    """处理 tool_calls 并返回最终文本"""

    messages.append(message)
    for tool_call in message.tool_calls or []:
        args = json.loads(tool_call.function.arguments)
        term = args.get("term", "")
        result = GLOSSARY.get(term, f"未找到: {term}")
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        })

    final = call_llm(messages, stream=False)
    return final.choices[0].message.content


def stream_reply(messages):
    """流式输出回复"""

    stream = call_llm(messages, stream=True)
    parts = []
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            parts.append(delta)
            print(delta, end="", flush=True)
    print()
    return "".join(parts)


def chat_loop():
    """CLI 主循环"""

    print("AI 专家 Agent v1（输入 exit 退出）")
    print("=" * 60)

    messages = [{"role": "system", "content": AI_EXPERT_SYSTEM}]

    while True:
        user_input = input("\n你>> ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        response = call_llm(messages, stream=False)
        choice = response.choices[0]

        if choice.finish_reason == "tool_calls":
            print("\nAI>> ", end="")
            answer = handle_tool_calls(choice.message, messages)
            print(answer)
            messages.append({"role": "assistant", "content": answer})
        else:
            print("\nAI>> ", end="")
            answer = choice.message.content
            print(answer)
            messages.append({"role": "assistant", "content": answer})

    print(f"\n本次会话累计 tokens（非流式部分）: {SESSION_TOKENS}")


if __name__ == "__main__":
    print("🚀 示例 9: AI 专家 Agent v1\n")
    chat_loop()
    print("\n✅ 示例运行完成！")
