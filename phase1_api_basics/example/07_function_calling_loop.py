"""
==========================================
示例 7: Function Calling 循环（多轮 tool）
==========================================
学习目标：
1. 根据 finish_reason 分支处理
2. while 循环直到 stop
3. 支持多步 tool 调用
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GLOSSARY = {
    "RAG": "检索增强生成（Retrieval-Augmented Generation）。",
    "Agent": "能自主调用工具完成任务的 LLM 应用架构。",
    "Prompt": "发送给模型的指令与上下文。",
}


def lookup_glossary(term):
    return GLOSSARY.get(term, f"未知术语: {term}")


def recommend_topic(level):
    topics = {
        "beginner": ["Prompt 基础", "API 调用", "Token 概念"],
        "intermediate": ["RAG", "Function Calling", "LangChain"],
    }
    return ", ".join(topics.get(level, topics["beginner"]))


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
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_topic",
            "description": "推荐学习主题列表",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "enum": ["beginner", "intermediate"],
                    }
                },
                "required": ["level"],
            },
        },
    },
]

TOOL_HANDLERS = {
    "lookup_glossary": lambda args: lookup_glossary(args["term"]),
    "recommend_topic": lambda args: recommend_topic(args["level"]),
}


def execute_tool_call(tool_call):
    """执行单个 tool call"""

    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        return f"未知工具: {name}"
    return handler(args)


def agent_loop(user_input, max_rounds=10):
    """Agent 主循环"""

    messages = [
        {"role": "system", "content": "你是 AI 学习导师，可查询术语并推荐学习主题。"},
        {"role": "user", "content": user_input},
    ]

    for _ in range(max_rounds):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        choice = response.choices[0]
        messages.append(choice.message)

        if choice.finish_reason == "stop":
            return choice.message.content

        if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
            for tool_call in choice.message.tool_calls:
                result = execute_tool_call(tool_call)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })
            continue

        return choice.message.content

    return "达到最大轮次"


if __name__ == "__main__":
    print("🚀 示例 7: Function Calling 循环\n")

    answer = agent_loop(
        "先查一下 RAG 的定义，然后给我推荐 intermediate 级别的学习主题，最后总结学习建议。"
    )
    print(answer)
    print("\n✅ 示例运行完成！")
