"""
==========================================
示例 6: Function Calling 基础（单轮）
==========================================
学习目标：
1. 定义 tools  schema
2. 处理 tool_calls 响应
3. 将 tool 结果回传完成对话

AI 专家变式：lookup_glossary 查询 AI 术语
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GLOSSARY = {
    "RAG": "检索增强生成，通过检索外部知识增强 LLM 回答。",
    "Agent": "能感知、推理并调用工具完成目标的智能体系统。",
    "Embedding": "将文本映射为向量，用于语义检索。",
}


def lookup_glossary(term):
    """查询 AI 术语表"""

    return GLOSSARY.get(term, f"未找到术语: {term}")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_glossary",
            "description": "查询 AI 相关术语的定义",
            "parameters": {
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "术语名称，如 RAG、Agent",
                    }
                },
                "required": ["term"],
            },
        },
    }
]


def run_tool_call(messages):
    """单轮 tool call 闭环"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message
    tool_calls = message.tool_calls

    if not tool_calls:
        return message.content

    messages.append(message)

    for tool_call in tool_calls:
        if tool_call.function.name == "lookup_glossary":
            args = json.loads(tool_call.function.arguments)
            result = lookup_glossary(args["term"])
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
    )
    return final.choices[0].message.content


if __name__ == "__main__":
    print("🚀 示例 6: Function Calling 基础\n")

    messages = [
        {"role": "system", "content": "你是 AI 技术导师，需要查术语时使用工具。"},
        {"role": "user", "content": "请解释 RAG 是什么，并结合 Agent 的关系说明。"},
    ]

    answer = run_tool_call(messages)
    print(answer)
    print("\n✅ 示例运行完成！")
