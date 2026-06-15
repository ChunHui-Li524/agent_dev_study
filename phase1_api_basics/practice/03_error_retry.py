"""
练习 03: 错误处理与重试
对应 example: example/03_error_retry.py
学习目标: 超时、限流、指数退避
完成日期:2026/06/14
自检: [√] 闭卷重写  [√] 变式完成  [√] 运行通过

变式要求（AI 专家 Agent）: 封装 call_llm() 供后续复用
"""
import os
import time

from dotenv import load_dotenv
from openai import Client, RateLimitError, OpenAIError


load_dotenv()


def call_llm(messages, temperature=0.7, max_retries=3):
    client = Client(
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )
    for attempt in range(max_retries):
        try:
            response = _chat(client, messages, temperature)
        except RuntimeError as e:
            wait = 2 ** attempt
            print(f"第{attempt}次模型调用失败, {wait}秒后重试：{e}")
            time.sleep(wait)
        else:
            return response

    raise RuntimeError(f"{max_retries}次尝试后模型调用失败")


def _chat(client, messages, temperature):
    try:
        chat = client.chat.completions.create(
            model="qwen3.6-27b",
            messages=messages,
            temperature=temperature,
            stream=False
        )
    except RateLimitError as e:
        raise RuntimeError(f"模型限流，请稍后再试：{e}")
    except OpenAIError as e:
        raise RuntimeError(f"调用模型中遇到错误：{e}")

    if not chat.choices:
        raise RuntimeError(f"模型未返回有效内容")

    return chat.choices[0].message.content


def ask_ai_expert_with_retry(question, max_retries=3):
    messages = [
        {"role": "system", "content": "你是AI领域专家，用通俗生动的话回答用户的问题"},
        {"role": "user", "content": question},
    ]
    try:
        return call_llm(messages, temperature=0.8, max_retries=max_retries)
    except RuntimeError as e:
        return f"模型调用失败：{e}"


if __name__ == "__main__":
    print(ask_ai_expert_with_retry("简要解释下MOE"))

# ============================================================
# 评卷意见（AI课程评卷老师 | 2026-06-14）
# 结论: 通过 ✅  |  得分: 90/100
# 运行验证: PyCharm 运行通过（exit code 0，MoE 问答正常）
# ------------------------------------------------------------
# 优点:
#   - call_llm() + _chat() 分层清晰，可供后续练习复用
#   - 指数退避（2 ** attempt）与 max_retries 逻辑正确
#   - RateLimitError / OpenAIError 分类捕获，空 choices 有防护
#   - ask_ai_expert_with_retry 外层兜底，AI 专家 persona 到位
# 待改进:
#   1. 补 timeout 参数并捕获 APITimeoutError / APIConnectionError
#   2. 401 认证错误不宜与限流/网络错误同样重试，应直接提示检查 .env
#   3. 重试日志建议用 attempt + 1，避免显示「第 0 次失败」
#   4. 文件头补完成日期，自检项勾选 [√]
# 检查项:
#   [√] 封装 call_llm() 并指数退避
#   [√] 限流（429）处理
#   [√] AI 专家 persona
#   [√] 通义千问环境变量
#   [√] 可独立运行
#   [ ] 超时（timeout）专项处理
#   [ ] 401/429/timeout 处理思路（代码或注释中说明）
# ============================================================
