"""
练习 06: Function Calling 基础
对应 example: example/06_function_calling_basic.py
学习目标: 单轮 tool 闭环
完成日期:2026/06/14
自检: [√] 闭卷重写  [√] 变式完成  [√] 运行通过

变式要求（AI 专家 Agent）: lookup_glossary 工具
"""
import json
import os

from dotenv import load_dotenv
from openai import Client

load_dotenv()

GLOSSARY = {
    "AI (人工智能)": "Artificial Intelligence的缩写，指让计算机系统模拟人类智能行为的技术，使其能够执行理解语言、识别图像、自主决策等通常需要人类智能才能完成的任务。",
    "LLM (大语言模型)": "Large Language Model的缩写，是一种基于海量文本数据训练而成的超大规模深度学习模型。它具备强大的自然语言理解与生成能力，能够像人类一样进行流畅的对话、文本创作和逻辑推理。",
    "AIGC (人工智能生成内容)": "AI-Generated Content的缩写，指利用人工智能算法自动生成文本、图像、音频、视频等具有创意和质量的内容，代表了从“内容消费”向“内容创造”的技术范式转变。",
    "Prompt (提示词)": "用户向AI模型发出的输入指令或引导语。通过精心设计提示词，可以明确任务目标、设定角色或规定输出格式，从而引导大模型更精准地理解需求并生成符合预期的结果。",
    "RAG (检索增强生成)": "Retrieval-Augmented Generation的缩写，是一种结合了外部知识库检索与大语言模型生成的技术。它能在模型生成回答前，先从指定数据源中检索相关信息作为上下文，从而有效减少模型“幻觉”，提高回答的准确性和时效性。"
}


def lookup_glossary(keyword):
    print(f"lookup_glossary called for [{keyword}]")
    global GLOSSARY
    for key, value in GLOSSARY.items():
        if keyword in key:
            return value
    return "未找到相关关键词"


TOOLs = [
    {
        "type": "function",
        "function": {
            "name": "lookup_glossary",
            "description": "从用户的私有知识库中查询相关关键词的说明",
            # 标准 parameters 格式（JSON Schema，见 OpenAI Function Calling 指南）：
            # "parameters": {
            #     "type": "object",
            #     "properties": {
            #         "keyword": {
            #             "type": "string",
            #             "description": "要查询的术语，如 LLM、RAG、Agent",
            #         }
            #     },
            #     "required": ["keyword"],
            # },
            # 查阅：example/06_function_calling_basic.py
            #      https://platform.openai.com/docs/guides/function-calling
            "parameters": {
                "keyword": "str"
            },
            "strict": True
        }
    }
]


def main():
    # 本次练习忽略异常处理
    client = Client(
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )

    questions = [
        "解释一下LLM",
        "解释一下Agent",
    ]

    for question in questions:
        print(f"[User]: {question}")
        messages = [
            {"role": "system",
             "content": "你是一个AI专家，用精简的话回答用户的提问。优先根据查询术语表解释，若无对应关键词，再根据你的知识回答"},
            {"role": "user", "content": question},
        ]
        response = ask(client, messages)
        response = process_tool_call(client, messages, response)
        print(f"[AI]: {response.choices[0].message.content}")


def ask(client, messages):
    response = client.chat.completions.create(
        messages=messages,
        model="qwen3.6-27b",
        temperature=0.3,
        stream=False,
        tools=TOOLs
    )
    return response


# ---------------------------------------------------------------------------
# tool call 处理 — 标准做法说明（练习 06 单轮闭环）
#
# 核心流程：用户消息 → 模型返回 tool_calls → 执行工具 → 回传 tool 消息 → 再请求 → 最终文本
#
# 标准写法要点：
#   1. 用 message.tool_calls 判断是否调工具（比仅看 finish_reason 更稳）
#   2. 先 append 完整的 assistant 消息（含 tool_calls，content 通常为 None）
#   3. for 循环内：逐个执行工具，append 对应的 tool 消息（tool_call_id 必须匹配）
#   4. 所有 tool 消息都 append 完后，再 ask() 一次（不要在循环内每处理一个就 ask）
#      原因：一次响应可能含多个并行 tool_call，必须全部回复后才能发起下一轮
#   5. 未知工具名也要有 tool 回复，否则第二轮 API 可能报错
#
# 标准写法参考（example/06_function_calling_basic.py）：
#   message = response.choices[0].message
#   if not message.tool_calls:
#       return response
#   messages.append(message)  # 或 {"role": "assistant", "content": None, "tool_calls": ...}
#   for tool_call in message.tool_calls:
#       if tool_call.function.name == "lookup_glossary":
#           args = json.loads(tool_call.function.arguments)
#           result = lookup_glossary(**args)
#           messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
#       else:
#           messages.append({"role": "tool", "tool_call_id": tool_call.id,
#                            "content": f"未知工具: {tool_call.function.name}"})
#   response = ask(client, messages)  # 循环结束后只请求一次
#   return response
#
# 练习 07 扩展：若第二次 ask 仍返回 tool_calls，需 while 循环，本练习 06 单轮即可。
# ---------------------------------------------------------------------------
def process_tool_call(client, messages, response):
    if response.choices[0].finish_reason == "tool_calls":
        messages.append({"role": "assistant", "tool_calls": response.choices[0].message.tool_calls})
        tool_calls = response.choices[0].message.tool_calls
        for tool_call in tool_calls:
            if tool_call.function.name == "lookup_glossary":
                parameters = json.loads(tool_call.function.arguments)
                result = lookup_glossary(**parameters)
                messages.append({"role": "tool", "content": result, "tool_call_id": tool_call.id})
                response = ask(client, messages)
    return response


if __name__ == "__main__":
    main()

# ============================================================
# 评卷意见（AI课程评卷老师 | 2026-06-14）
# 结论: 通过 ✅  |  得分: 88/100
# 运行验证: PyCharm 运行通过（lookup_glossary 调用 LLM/Agent，exit code 0）
# ------------------------------------------------------------
# 优点:
#   - 单轮 tool 闭环正确：assistant(tool_calls) → tool 消息 → 二次 ask
#   - lookup_glossary 变式完成，term in key 模糊匹配
#   - ask / process_tool_call / main 分层清晰
#   - 文件内已注释标准 parameters schema 与 tool call 标准写法
# 待改进:
#   1. parameters 建议改为标准 JSON Schema（见上方注释）
#   2. ask() 建议移到 for tool_call 循环外（多 tool 并行时更稳）
#   3. assistant 消息建议 content: None + tool_calls
# 检查项:
#   [√] 单轮 tool 闭环
#   [√] lookup_glossary 变式
#   [√] 处理 tool_calls 并回传 tool 消息
#   [√] AI 专家 persona
#   [√] 通义千问环境变量
#   [√] 可独立运行
#   [ ] parameters 标准 JSON Schema（当前为简写格式）
# ============================================================
