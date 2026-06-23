"""
练习 07: Tool 循环
对应 example: example/07_function_calling_loop.py
学习目标: finish_reason 分支
完成日期:2026/06/14
自检: [√] 闭卷重写  [√] 变式完成  [√] 运行通过

变式要求（AI 专家 Agent）: 多步查术语+推荐主题
"""
import json
import os
from json import JSONDecodeError
from typing import List

from dotenv import load_dotenv
from openai import Client
from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion import Choice

load_dotenv()

GLOSSARY = {
    "AI (人工智能)": "Artificial Intelligence的缩写，指让计算机系统模拟人类智能行为的技术，使其能够执行理解语言、识别图像、自主决策等通常需要人类智能才能完成的任务。",
    "LLM (大语言模型)": "Large Language Model的缩写，是一种基于海量文本数据训练而成的超大规模深度学习模型。它具备强大的自然语言理解与生成能力，能够像人类一样进行流畅的对话、文本创作和逻辑推理。",
    "AIGC (人工智能生成内容)": "AI-Generated Content的缩写，指利用人工智能算法自动生成文本、图像、音频、视频等具有创意和质量的内容，代表了从“内容消费”向“内容创造”的技术范式转变。",
    "Prompt (提示词)": "用户向AI模型发出的输入指令或引导语。通过精心设计提示词，可以明确任务目标、设定角色或规定输出格式，从而引导大模型更精准地理解需求并生成符合预期的结果。",
    "RAG (检索增强生成)": "Retrieval-Augmented Generation的缩写，是一种结合了外部知识库检索与大语言模型生成的技术。它能在模型生成回答前，先从指定数据源中检索相关信息作为上下文，从而有效减少模型“幻觉”，提高回答的准确性和时效性。"
}


AI_THEMES = {
    "初学": [
        "Python编程基础与数据处理（NumPy, Pandas）",
        "机器学习核心概念与经典算法（线性回归, 决策树, SVM）",
        "Scikit-learn框架实战与模型评估",
        "数据可视化与探索性数据分析（Matplotlib, Seaborn）",
        "AI数学基础（线性代数, 概率论, 微积分）"
    ],
    "进阶": [
        "深度学习框架实战（PyTorch / TensorFlow）",
        "计算机视觉（CNN, 目标检测, 图像分割）",
        "自然语言处理（RNN, LSTM, Attention机制）",
        "模型调优与超参数搜索策略",
        "特征工程与数据管道构建"
    ],
    "高级": [
        "大语言模型（LLM）原理与微调（LoRA, RLHF）",
        "Transformer架构深度解析与自研实现",
        "分布式训练与模型并行（DeepSpeed, FSDP）",
        "AI系统部署与推理优化（TensorRT, vLLM）",
        "前沿论文复现与AI Agent开发"
    ]
}


def lookup_glossary(term):
    for key, value in GLOSSARY.items():
        if term in key:
            return value
    return f"未找到术语【{term}】"


def get_themes(level):
    try:
        themes = AI_THEMES[level]
        return ", ".join(themes)
    except KeyError:
        return "未找到对应等级的推荐"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_glossary",
            "description": "查询AI相关的术语表",
            "parameters": {
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "要查询的主题"
                    }
                },
                "required": ["term"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_themes",
            "description": "查询AI学习不同阶段需要的基础",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "description": "阶段的名称，固定三种",
                        "enum": ["初学", "进阶", "高级"]
                    }
                },
                "required": ["level"]
            }
        }
    }
]


class ToolCallAgent:
    def __init__(self):
        self.client = Client(
            base_url=os.getenv("DASHSCOPE_BASE_URL"),
            api_key=os.getenv("DASHSCOPE_API_KEY")
        )
        self._messages = [
            {"role": "system", "content": "你是一个AI培训老师，负责为用户提供AI学习建议"}
        ]
        self._tools = {
            "lookup_glossary": lookup_glossary,
            "get_themes": get_themes,
        }

    def chat(self, question):
        self._messages.append({"role": "user", "content": question})

        for i in range(20):
            choice = self._chat()

            if choice.finish_reason == "stop":
                return choice.message.content

            if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                self._messages.append({"role": "assistant", "content": None, "tool_calls": choice.message.tool_calls})
                self._run_tool_calls(choice.message.tool_calls)

        return "达到最大调用次数"

    def _chat(self) -> Choice:
        # 本次练习忽略超时、401、429等异常处理
        response = self.client.chat.completions.create(
            messages=self._messages,
            model="qwen3.6-27b",
            temperature=0.5,
            stream=False,
            tools=TOOLS
        )
        return response.choices[0]

    def _run_tool_calls(self, toolcalls: List[ChatCompletionMessageToolCall]):
        for toolcall in toolcalls:
            message = {"role": "tool", "tool_call_id": toolcall.id}
            if toolcall.function.name in self._tools:
                message["content"] = self._call_tool(toolcall)
            else:
                message["content"] = f"TOOL不存在"
            self._messages.append(message)

    def _call_tool(self, toolcall):
        try:
            arguments = json.loads(toolcall.function.arguments)
            func = self._tools[toolcall.function.name]
            result = func(**arguments)
            print(f"调用[{toolcall.function.name}]: {arguments}")
            return result
        except (JSONDecodeError, TypeError) as e:
            print(f"TOOL调用失败: {e}")
            return f"TOOL调用失败: {e}"


if __name__ == "__main__":
    agent = ToolCallAgent()
    print(agent.chat("先查一下 RAG 的定义，再推荐高级学习主题，最后总结学习计划。"))

# ============================================================
# 评卷意见（AI课程评卷老师 | 2026-06-14）
# 结论: 通过 ✅  |  得分: 98/100
# 运行验证: PyCharm 运行通过（lookup_glossary + get_themes 并行调用，exit code 0）
# ------------------------------------------------------------
# 优点:
#   - ToolCallAgent 循环：finish_reason 分支 + 多轮 _chat() 标准
#   - 全部 tool 消息 append 后再进入下一轮，符合 example 写法
#   - 两工具 lookup_glossary + get_themes，变式「查术语+推荐主题」完整演示
#   - lookup_glossary 改为 term in key 模糊匹配，RAG 可正确命中
#   - 标准 JSON Schema、未知 tool 兜底、JSONDecodeError/TypeError 捕获
# 待改进:
#   1. _chat() 可对 response.choices 为空做轻量 guard
#   2. 其他 finish_reason（length 等）可单独处理，避免空转 max rounds
# 检查项:
#   [√] 定义 tools schema
#   [√] 处理 tool_calls 并回传 tool 消息
#   [√] 根据 finish_reason 循环
#   [√] 多步查术语 + 推荐主题（变式）
#   [√] 通义千问环境变量
#   [√] 可独立运行
# ============================================================
