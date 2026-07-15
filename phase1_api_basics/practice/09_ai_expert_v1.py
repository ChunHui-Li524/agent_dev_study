"""
练习 09: AI 专家 v1 综合
对应 example: example/09_ai_expert_v1.py
学习目标: 串联 Phase 1 能力
完成日期:2026/06/14
自检: [√] 闭卷重写  [√] 变式完成  [√] 运行通过

变式要求（AI 专家 Agent）: CLI 流式+工具+重试+token
"""

import json
import os
from json import JSONDecodeError

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

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
        # 参考：persona 可用中文，与主线「AI 专家 Agent」一致
        # {"role": "system", "content": "你是 AI 技术导师，优先用 lookup_glossary 查询术语，再用中文简洁回答。"}
        self._messages = [
            {"role": "system", "content": "You are an AI expert, search and shortly answer user`s question with chinese"},
        ]

    def chat(self, question, max_iter=20):
        self._messages.append({"role": "user", "content": question})
        total = 0
        for i in range(max_iter):
            try:
                is_stop, token = self._process_stream()
                print(f"\nSystem: 本轮（第{i+1}轮）消耗token：{token}")
                total += token
            except OpenAIError as e:
                # 此处当前简化，统一处理所有异常
                print(f"Agent访问异常，重试中：{e}")
                # ----------------------------------------------------------------
                # 参考写法 3：真正的指数退避重试（对「同一次」API 调用，而不是空 continue）
                # import time
                # from openai import RateLimitError, APITimeoutError, APIConnectionError
                # for attempt in range(3):
                #     try:
                #         return self._process_stream()
                #     except (RateLimitError, APITimeoutError, APIConnectionError) as err:
                #         wait = 2 ** attempt
                #         print(f"可重试错误: {err}，{wait}s 后重试 ({attempt + 1}/3)")
                #         time.sleep(wait)
                # raise RuntimeError("重试耗尽仍失败")
                # 说明：401/AuthenticationError 不宜退避重试，应直接提示检查 .env
                # ----------------------------------------------------------------
                continue

            if is_stop:
                # 参考写法：会话结束时可打印累计 token
                # print(f"System: 本问题累计 token：{total}")
                return
        else:
            print(f"Error: 模型流式返回异常，达到最大迭代次数")

    def _process_stream(self):
        stream_response = self.client.chat.completions.create(
            messages=self._messages,
            model="qwen3.6-27b",
            temperature=0.5,
            stream=True,
            tools=TOOLS
            # ----------------------------------------------------------------
            # 参考写法 2：流式请求开启 usage，避免本轮 token 常为 0
            # stream_options={"include_usage": True},  # 通义兼容接口通常支持
            # 或：在最后一个无 choices、仅带 usage 的 chunk 中累加
            # ----------------------------------------------------------------
        )
        delta_tool_calls = []
        # 参考写法 1+5：累积正式回答，过滤思考链，停顿时写入 messages
        # content_parts = []
        token = 0
        for chunk in stream_response:
            if chunk.usage:
                token += chunk.usage.total_tokens
            if chunk.choices:
                delta = chunk.choices[0].delta
                # ----------------------------------------------------------------
                # 参考写法 1：过滤思考链 / reasoning，只打印最终回答
                # Qwen 等模型可能通过 reasoning_content 或 content 泄漏思考过程
                # reasoning = getattr(delta, "reasoning_content", None)
                # if reasoning:
                #     continue  # 或写入调试日志，不要 print 到 CLI
                # if delta.content:
                #     content_parts.append(delta.content)
                #     print(delta.content, end="", flush=True)
                # ----------------------------------------------------------------
                if delta.content:
                    print(delta.content, end="")
                if delta.tool_calls:
                    delta_tool_calls.extend(delta.tool_calls)
                if chunk.choices[0].finish_reason == "tool_calls":
                    merged = self._merge_tool_call(delta_tool_calls)
                    # 参考写法 4：合并后按 id 或 (name, arguments) 去重，避免同一工具执行两次
                    # seen, unique = set(), []
                    # for info in merged:
                    #     key = (info["id"],) or (info["function"]["name"], info["function"]["arguments"])
                    #     if key in seen:
                    #         continue
                    #     seen.add(key)
                    #     unique.append(info)
                    # merged = unique
                    self._messages.append({"role": "assistant", "content": None, "tool_calls": merged})
                    self._call_tool(merged)
                elif chunk.choices[0].finish_reason == "stop":
                    # ----------------------------------------------------------------
                    # 参考写法 5：终局回答写入 messages，保证多轮上下文完整
                    # final_text = "".join(content_parts)
                    # self._messages.append({"role": "assistant", "content": final_text})
                    # return True, token
                    # ----------------------------------------------------------------
                    return True, token
        return False, token

    def _call_tool(self, merged):
        for info in merged:
            func = info["function"]
            print(f"Agent请求调用工具：{func['name']}")
            tool_result = get_tool_result(func["name"], func["arguments"])
            print(f"工具返回结果：{tool_result}")
            self._messages.append({
                "role": "tool",
                "tool_call_id": info["id"],
                "content": tool_result,
            })

    def _merge_tool_call(self, delta_tool_calls):
        # ----------------------------------------------------------------
        # 参考写法 4（合并侧）：按 index 合并后建议 sorted(merged.items()) 保证顺序
        # return [
        #     {"id": v["id"], "type": "function",
        #      "function": {"name": v["name"], "arguments": v["arguments"]}}
        #     for _, v in sorted(merged.items())
        # ]
        # ----------------------------------------------------------------
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


def run_cli():
    agent = StreamToolCallAgent()
    user_input = input("Agent：你好，我是AI Agent专家，你有什么问题需要问我？\n")
    while user_input != "exit":
        agent.chat(user_input)
        user_input = input("[System] Agent回答结束，请继续对话或退出\n")
    print("ThankYou, 即将退出")


if __name__ == "__main__":
    run_cli()

# ============================================================
# 评卷意见（AI课程评卷老师 | 2026-06-14）
# 结论: 通过 ✅  |  得分: 86/100
# 运行验证: PyCharm 运行通过（CLI 对话 + tool + exit code 0）
# ------------------------------------------------------------
# 优点:
#   - CLI + 流式 + 流式 tool 拼接 + 多轮对话，综合 v1 主线达成
#   - 复用 08 的 merge/call 结构，max_iter 防无限循环
#   - 至少串联流式、工具、token 日志尝试（checklist ≥3 项）
# 待改进:（参考写法已写在对应代码旁，未改动业务逻辑）
#   1. 过滤思考链 / reasoning，只打印最终回答
#   2. stream_options include_usage，避免 token 常为 0
#   3. 指数退避重试；401 不重试
#   4. tool 合并后按 id/(name,args) 去重，避免重复调用
#   5. finish_reason=stop 时把 assistant content 写入 messages
#   6. （可选）system 提示改中文 AI 专家 persona
# 检查项:
#   [√] CLI 可交互运行
#   [√] 流式输出
#   [√] 流式 tool 闭环
#   [√] Token 日志尝试（实测偶发为 0）
#   [ ] 完整指数退避重试
#   [√] 通义千问环境变量
# ============================================================
