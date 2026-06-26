"""
练习 08: 流式 Tool Call
对应 example: example/08_stream_tool_call.py
学习目标: 拼接 tool_calls 增量
完成日期:2026/06/14
自检: [√] 闭卷重写  [√] 变式完成  [√] 运行通过

变式要求（AI 专家 Agent）: 整理为可复用函数
"""
import json
import os
from json import JSONDecodeError

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


GLOSSARY = {
    "AI (人工智能)": "Artificial Intelligence的缩写，指让计算机系统模拟人类智能行为的技术，使其能够执行理解语言、识别图像、自主决策等通常需要人类智能才能完成的任务。",
    "LLM (大语言模型)": "Large Language Model的缩写，是一种基于海量文本数据训练而成的超大规模深度学习模型。它具备强大的自然语言理解与生成能力，能够像人类一样进行流畅的对话、文本创作和逻辑推理。",
    "AIGC (人工智能生成内容)": "AI-Generated Content的缩写，指利用人工智能算法自动生成文本、图像、音频、视频等具有创意和质量的内容，代表了从“内容消费”向“内容创造”的技术范式转变。",
    "Prompt (提示词)": "用户向AI模型发出的输入指令或引导语。通过精心设计提示词，可以明确任务目标、设定角色或规定输出格式，从而引导大模型更精准地理解需求并生成符合预期的结果。",
    "RAG (检索增强生成)": "Retrieval-Augmented Generation的缩写，是一种结合了外部知识库检索与大语言模型生成的技术。它能在模型生成回答前，先从指定数据源中检索相关信息作为上下文，从而有效减少模型“幻觉”，提高回答的准确性和时效性。"
}


def lookup_glossary(term):
    print("tool called")
    for key, value in GLOSSARY.items():
        if term in key:
            return value
    return f"未找到术语【{term}】"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_glossary",
            "description": "lookup glossary of AI",
            "parameters": {
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "the key glossary of AI"
                    }
                },
                "required": ["term"],
            }
        }
    }
]


def get_tool_result(name, arguments_txt):
    if name != "lookup_glossary":
        return f"未知工具：{name}"
    try:
        arguments = json.loads(arguments_txt)
        return lookup_glossary(**arguments)
    except JSONDecodeError as e:
        return f"工具[{name}]参数格式不正确: {e}"


class StreamToolCallAgent:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("DASHSCOPE_BASE_URL"),
            api_key=os.getenv("DASHSCOPE_API_KEY"),
        )
        self._messages = [
            {"role": "system", "content": "You are an AI expert, search and shortly answer user`s question with chinese"},
        ]

    def chat(self, question):
        self._messages.append({"role": "user", "content": question})
        for i in range(20):
            result = self._process_stream()
            if result is not None:
                return result
        return "模型流式返回异常，达到最大迭代次数"

    def _process_stream(self, ):
        stream_response = self.client.chat.completions.create(
            messages=self._messages,
            model="qwen3.6-27b",
            temperature=0.5,
            stream=True,
            tools=TOOLS
        )
        delta_tool_calls = []
        content = []
        for chunk in stream_response:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta.content:
                    content.append(delta.content)
                if delta.tool_calls:
                    delta_tool_calls.extend(delta.tool_calls)
                if chunk.choices[0].finish_reason == "tool_calls":
                    merged = self._merge_tool_call(delta_tool_calls)
                    self._messages.append({"role": "assistant", "content": None, "tool_calls": merged})
                    self._call_tool(merged)
                elif chunk.choices[0].finish_reason == "stop":
                    return "".join(content)
        return None

    def _call_tool(self, merged):
        for info in merged:
            func = info["function"]
            tool_result = get_tool_result(func["name"], func["arguments"])
            self._messages.append({
                "role": "tool",
                "tool_call_id": info["id"],
                "content": tool_result,
            })

    def _merge_tool_call(self, delta_tool_calls):
        merged = {}
        for delta_tool_call in delta_tool_calls:
            idx = delta_tool_call.index
            function = delta_tool_call.function
            if idx not in merged:
                merged[idx] = {"id": "", "name": "", "arguments": ""}

            if delta_tool_call.id:
                merged[idx]["id"] = delta_tool_call.id
            if function.name:
                merged[idx]["name"] += function.name
            if function.arguments:
                merged[idx]["arguments"] += function.arguments

        return [
            {
                "id": call["id"],
                "type": "function",
                "function": {"name": call["name"], "arguments": call["arguments"]},
            }
            for call in merged.values()
        ]



if __name__ == "__main__":
    agent = StreamToolCallAgent()
    print(agent.chat("解释一下AIGC"))

# ============================================================
# 评卷意见（AI课程评卷老师 | 2026-06-14）
# 结论: 通过 ✅  |  得分: 94/100
# 运行验证: 语法检查通过（py_compile）
# ------------------------------------------------------------
# 优点:
#   - _merge_tool_call 按 index 拼接 id/name/arguments，逻辑正确
#   - StreamToolCallAgent 可复用，变式「整理为可复用函数」到位
#   - 流式 tool 后回传 messages 并二次流式请求，闭环比 example 更完整
#   - get_tool_result 独立处理 JSON 解析与工具分发
# 待改进:
#   1. 流式 content 可实时 print，增强流式体验
#   2. finish_reason 建议在流结束后统一处理
#   3. 多 tool 时 merged 建议 sorted(merged.items()) 保序
#   4. system 提示可统一为中文 AI 专家 persona
# 检查项:
#   [√] stream=True 流式请求
#   [√] 拼接 tool_calls 增量
#   [√] finish_reason tool_calls 执行工具
#   [√] tool 后再次请求拿最终回答
#   [√] 可复用函数/类封装
#   [√] 通义千问环境变量
# ============================================================
