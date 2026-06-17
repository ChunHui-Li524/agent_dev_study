"""
练习 04: Token 统计
对应 example: example/04_token_usage.py
学习目标: usage 字段与成本估算
完成日期:2026/06/14
自检: [√] 闭卷重写  [√] 变式完成  [√] 运行通过

变式要求（AI 专家 Agent）: 每次对话打印 token
"""
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import Client, RateLimitError, AuthenticationError, OpenAIError
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletion


TOKEN_PRICE = {
    "qwen3.6-27b": {"input": 0.15, "output": 0.3}
}


load_dotenv()


@dataclass
class TokenCost:
    total_token: int = 0
    input_token: int = 0
    input_cost: float = 0
    output_token: int = 0
    output_cost: float = 0

    def total_cost(self):
        return self.input_cost + self.output_cost

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("类型不匹配")

        return TokenCost(
            self.total_token + other.total_token,
            self.input_token + other.input_token,
            self.input_cost + other.input_cost,
            self.output_token + other.output_token,
            self.output_cost + other.output_cost,
        )

    def print_cost(self):
        print(f"[Cost] 总消耗token：{self.total_token}, 花费{self.total_cost()}元")
        print(f"[Cost] ----输入token：{self.input_token}, 花费{self.input_cost}元")
        print(f"[Cost] ----输出token：{self.output_token}, 花费{self.output_cost}元")


def ask_questions_with_cost(questions: list):
    client = Client(
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    messages = [
        {"role": "system", "content": "你是一个AI专家，用通俗生动的方式回答用户的问题"},
    ]

    total_token_cost = TokenCost()
    for question in questions:
        messages.append({"role": "user", "content": question})
        try:
            response = chat(client, messages)
        except RuntimeError as e:
            print(e)
            continue

        if response.choices and response.choices[0].message.content:
            content = response.choices[0].message.content
            messages.append({"role": "assistant", "content": content})
            print(f"[Question] {question}")
            print(f"[Answer] {content}")

            if response.usage:
                token_cost = get_token_cost(response.model, response.usage)
                token_cost.print_cost()
                total_token_cost += token_cost

    print("-"*40)
    print("多轮对话消耗统计如下：")
    total_token_cost.print_cost()


def chat(client: Client, messages: list) -> ChatCompletion:
    try:
        response = client.chat.completions.create(
            model="qwen3.6-27b",
            messages=messages,
            stream=False,
            temperature=0.5
        )
    except RateLimitError as e:
        raise RuntimeError(f"模型限流，请稍后再试：{e}")
    except TimeoutError as e:
        raise RuntimeError(f"模型访问超时，请稍后再试：{e}")
    except AuthenticationError as e:
        raise RuntimeError(f"模型鉴权失败，请检查相关参数：{e}")
    except OpenAIError as e:
        raise RuntimeError(f"模型访问失败：{e}")

    return response


def get_token_cost(model, usage: CompletionUsage):
    model_price = TOKEN_PRICE.get(model, {"input": 0.1, "output": 0.1})
    input_price = model_price["input"]
    output_price = model_price["output"]
    return TokenCost(
        usage.total_tokens,
        usage.prompt_tokens,
        usage.prompt_tokens / 1_000_000 * input_price,
        usage.completion_tokens,
        usage.completion_tokens / 1_000_000 * output_price,
    )


if __name__ == "__main__":
    my_q = ["什么是Agent？", "如何自己搭建一个Agent"]
    ask_questions_with_cost(my_q)

# ============================================================
# 评卷意见（AI课程评卷老师 | 2026-06-14）
# 结论: 通过 ✅  |  得分: 97/100
# 运行验证: PyCharm 运行通过（exit code 0，两轮问答 + 多轮累计 5954 tokens）
# ------------------------------------------------------------
# 优点:
#   - TokenCost 数据类 + __add__ 累计设计清晰，超出 example 基础写法
#   - 每轮 [Question]/[Answer]/[Cost] 输出完整，变式「每次打印 token」到位
#   - 多轮 messages 累积后输入 token 增长符合预期，末尾汇总正确
#   - chat() 错误分类（限流/鉴权/API）可复用
# 待改进:
#   1. 超时建议捕获 APITimeoutError（SDK），而非内置 TimeoutError
#   2. print_cost 金额可用 :.6f 格式化，避免浮点展示冗长
#   3. 成本单价若为估算，可在注释中标注单位/来源
# 检查项:
#   [√] 读取 usage 字段
#   [√] 单次成本估算
#   [√] 每次对话打印 token
#   [√] 多轮累计 token
#   [√] AI 专家 persona
#   [√] 通义千问环境变量
#   [√] 可独立运行
# ============================================================
