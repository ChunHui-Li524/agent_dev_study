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

print(os.getenv("DASHSCOPE_API_KEY"))
print(os.getenv("DASHSCOPE_BASE_URL"))

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)


def practice_1():
    # 模型列表：https://help.aliyun.com/model-studio/getting-started/models
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "user", "content": "hello, 你是谁"}
        ]
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    practice_1()

