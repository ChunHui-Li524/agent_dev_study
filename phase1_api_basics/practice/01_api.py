# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2026-03-18
@Description: 
    This is a brief description of what the script does.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)


def practice_1():
    # 模型列表：https://help.aliyun.com/model-studio/getting-started/models
    response = client.chat.completions.create(
        model="qwen3.5-27b",
        messages=[
            {"role": "user", "content": "hello, 你是谁"}
        ]
    )
    print(response.choices[0].message.content)


def chat():
    """对话模式"""
    print("AI高级评茶师已启动，输入'exit'或'111'退出聊天")
    print("="*80)
    messages = [
        {"role": "system", "content": "你是一个专业的高级评茶师，对茶艺、工艺、各种茶的特性都有很深的理解，现在回答用户茶叶相关的问题"}
    ]
    while True:
        response = client.chat.completions.create(
            model="qwen3.5-27b",
            messages=messages
        )

        ai_response = response.choices[0].message.content
        print(f"{'AI高级评茶师>>':<8}", ai_response)
        print("-" * 80, end="\n\n")
        messages.append({"role": "assistant", "content": ai_response})

        user_input = input(f"{'你>>':<8}")
        if user_input.lower() == "exit" or user_input.lower() == "111":
            break
        print("-" * 80, end="\n\n")
        print(f"{'System>>':<8} 已接受到您的反馈，请稍后...", end="\n\n")
        print("-" * 80, end="\n\n")
        messages.append({"role": "user", "content": user_input})
    print("=" * 80)
    print("聊天已退出")


def stream_chat():
    """流式对话模式"""
    print("AI高级评茶师已启动，输入'exit'或'111'退出聊天")
    print("="*80)
    messages = [
        {"role": "system", "content": "你是一个专业的高级评茶师，对茶艺、工艺、各种茶的特性都有很深的理解，现在回答用户茶叶相关的问题"}
    ]
    while True:
        stream = client.chat.completions.create(
            model="qwen3.5-27b",
            messages=messages,
            stream=True
        )
        for chunk in stream:
            # print(chunk)
            txt = chunk.choices[0].delta.content
            if txt is not None:
                print(txt, end="", flush=True)

        print("\n-" * 80, end="\n\n")
        user_input = input(f"{'你>>':<8}")
        if user_input.lower() == "exit" or user_input.lower() == "111":
            break
        messages.append({"role": "user", "content": user_input})


if __name__ == '__main__':
    # practice_1()
    # chat()
    stream_chat()
