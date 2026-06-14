"""
练习 02: 流式输出
对应 example: example/02_openai_streaming.py
学习目标: stream、chunk 拼接
完成日期:2026/06/14
自检: [√] 闭卷重写  [√] 变式完成  [√] 运行通过

变式要求（AI 专家 Agent）: AI 专家流式问答，统计 chunk 数与耗时
"""


import os
import time


from dotenv import load_dotenv
from openai import Client
from openai.resources.beta.threads import Messages


load_dotenv()


def ai_expert_stream():
    """AI 专家流式问答"""
    client = Client(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_BASE_URL")
    )

    messages = [{
        "role": "system",
        "content": "你是一个AI专家，用简洁生动的语句答复用户相关的疑问"
    }]

    while True:
        stream = client.chat.completions.create(
            model="qwen3.6-27b",
            messages=messages,
            temperature=0.8,
            stream=True
        )

        full_answer = ""
        chunk_cnt = 0
        start_time = time.time()
        for chunk in stream:
            chunk_cnt += 1
            if not chunk.choices:
                break

            if chunk.choices[0].delta.content:
                txt = chunk.choices[0].delta.content
                print(txt, end="", flush=True)
                full_answer += txt

        messages.append({"role": "assistant", "content": full_answer})
        total_time = time.time() - start_time
        print(f"\nchunk count: {chunk_cnt}; time: {total_time}; per chunk: {total_time / chunk_cnt}")

        user_input = input("you：")
        if user_input.startswith("ex"):
            break
        messages.append({"role": "user", "content": user_input})

    print("AI专家已下线，感谢您的支持")     


if __name__ == "__main__":
    ai_expert_stream()


# ============================================================
# 评卷意见（AI课程评卷老师 | 2026-06-14）
# 结论: 通过 ✅  |  得分: 92/100
# ------------------------------------------------------------
# 优点:
#   - stream=True、chunk 遍历、内容拼接与实时打印均正确
#   - AI 专家 persona + chunk/耗时/均值统计完整，多轮对话符合主线
#   - 对 chunk.choices 为空做了 break，运行验证通过
# 待改进:
#   1. 删除未使用的 Messages import（第 16 行）
#   2. chunk_cnt 为 0 时 total_time / chunk_cnt 可能除零
#   3. （可选）首轮仅 system 消息即开始流式，模型会先自说自话；可先 input 再 stream
# 检查项:
#   [√] stream=True 并遍历 chunk
#   [√] delta.content 判空
#   [√] AI 专家 persona
#   [√] chunk 统计与耗时
#   [√] 通义千问环境变量
#   [√] 可独立运行
# ============================================================
