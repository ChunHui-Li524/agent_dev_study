"""
==========================================
示例 8: 流式 Function Calling
==========================================
学习目标：
1. stream=True 时拼接 tool_calls 增量
2. 区分 content / tool_calls / reasoning_content
3. 拼接完成后执行工具
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def lookup_glossary(term):
    return {"RAG": "检索增强生成", "Agent": "智能体"}.get(term, "未知")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_glossary",
            "description": "查询 AI 术语",
            "parameters": {
                "type": "object",
                "properties": {"term": {"type": "string"}},
                "required": ["term"],
            },
        },
    }
]


def merge_tool_call_deltas(tool_calls_chunk):
    """将流式 tool_calls 增量合并为完整调用"""

    merged = {}
    for delta_call in tool_calls_chunk:
        idx = delta_call.index
        if idx not in merged:
            merged[idx] = {"id": delta_call.id or "", "name": "", "arguments": ""}

        if delta_call.id:
            merged[idx]["id"] = delta_call.id
        if delta_call.function.name:
            merged[idx]["name"] += delta_call.function.name
        if delta_call.function.arguments:
            merged[idx]["arguments"] += delta_call.function.arguments

    return merged


def stream_with_tools(user_input):
    """流式请求并处理 tool calls"""

    messages = [{"role": "user", "content": user_input}]
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        stream=True,
    )

    content_parts = []
    tool_calls_chunk = []
    finish_reason = None

    for chunk in stream:
        choice = chunk.choices[0]
        delta = choice.delta

        if delta.content:
            content_parts.append(delta.content)
            print(delta.content, end="", flush=True)

        if delta.tool_calls:
            tool_calls_chunk.extend(delta.tool_calls)

        finish_reason = choice.finish_reason

    print()

    if finish_reason == "tool_calls":
        merged = merge_tool_call_deltas(tool_calls_chunk)
        for idx, call in sorted(merged.items()):
            args = json.loads(call["arguments"])
            if call["name"] == "lookup_glossary":
                result = lookup_glossary(args["term"])
                print(f"\n[Tool {idx}] lookup_glossary({args['term']}) => {result}")

    return "".join(content_parts), finish_reason


if __name__ == "__main__":
    print("🚀 示例 8: 流式 Function Calling\n")
    stream_with_tools("请查一下 RAG 是什么意思，并用一句话总结。")
    print("\n✅ 示例运行完成！")
