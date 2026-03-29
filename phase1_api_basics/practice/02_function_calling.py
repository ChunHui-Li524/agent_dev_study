# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2026-03-25
@Description: 
    This is a brief description of what the script does.
"""
import json
import logging
import os
from pprint import pprint

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.Logger("02_tool_call")
logger.addHandler(logging.StreamHandler())


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)


def create_file(path, content):
    logger.info("AI调用tool 【create_file】")
    logger.debug(f"path: {path}")
    logger.debug(f"content: {content}")


tools = [
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "用于创建文件，将指定的内容写入到指定文件中",
            "parameters": {
                "path": "创建的文件地址，str类型",
                "content": "要写入文件的内容，str类型"
            },
            "strict": True
        }
    }
]


def block_function_call():
    messages = [{"role": "user", "content": "把李白的静夜思写到文件中，路径，文件名你决定"}]
    response = client.chat.completions.create(
        model="qwen3.5-27b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    tool_calls = response.choices[0].message.tool_calls
    pprint(response.choices[0])
    if tool_calls is not None:
        # 首先将 AI 的响应（包含 tool_calls）添加到 messages 中
        messages.append(response.choices[0].message)
        logger.debug(f"AI调用工具：{response.choices[0].message}")

        for tool_call in tool_calls:
            if tool_call.function.name == "create_file":
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except ValueError as e:
                    logger.error(e)
                    logger.error(f"LLM 返回的tool call参数有误：{tool_call.function.arguments}")
                    return
                create_file(arguments["path"], arguments["content"])
                messages.append({"role": "tool", "content": "文件已写入，操作正常", "tool_call_id": tool_call.id})
        
        # 现在继续对话
        response = client.chat.completions.create(
            model="qwen3.5-27b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
    logger.info(response.choices[0].message.content)
    if response.choices[0].finish_reason == "stop":
        logger.info("AI执行完成")


def block_function_call_2():
    messages = [{"role": "user", "content": "把李白的静夜思写到文件中，路径，文件名你决定"}]
    while True:
        response = client.chat.completions.create(
            model="qwen3.5-27b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        messages.append(response.choices[0].message)
        if response.choices[0].finish_reason == "stop":
            logger.info(response.choices[0].message.content)
            user_input = input("请输入>>")
            if user_input == "1":
                return
            messages.append({"role": "user", "content": user_input})
        elif response.choices[0].finish_reason == "tool_calls":
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls is not None:
                # 首先将 AI 的响应（包含 tool_calls）添加到 messages 中
                logger.debug(f"AI请求调用工具：{response.choices[0].message}")
                for tool_call in tool_calls:
                    if tool_call.function.name == "create_file":
                        try:
                            arguments = json.loads(tool_call.function.arguments)
                        except ValueError as e:
                            logger.error(e)
                            logger.error(f"LLM 返回的tool call参数有误：{tool_call.function.arguments}")
                            return
                        create_file(arguments["path"], arguments["content"])
                        messages.append({"role": "tool", "content": "文件已写入，操作正常", "tool_call_id": tool_call.id})
        else:
            logger.error(f"LLM返回当前不支持的中断：{response.choices[0].finish_reason}")


def stream_function_call():
    messages = [{"role": "user", "content": "把李白的静夜思写到文件中，路径，文件名你决定"}]
    stream = client.chat.completions.create(
        model="qwen3.5-27b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        stream=True
    )

    content_chunk = []
    tool_calls_chunk = []
    reasoning_content_chunk = []
    finish_reason = None
    for chunk in stream:
        choice = chunk.choices[0]
        pprint(choice)
        if choice.delta.content:
            content_chunk.append(choice.delta.content)
            print(choice.delta.content, end="")

        """
        Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None,
            tool_calls=[
                ChoiceDeltaToolCall(
                    index=0, id='call_9f4aa1a39d164d11a2865e68',
                    function=ChoiceDeltaToolCallFunction(arguments='', name='create_file'),
                    type='function')
            ],
            reasoning_content=None), finish_reason=None, index=0, logprobs=None)
        Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None,
            tool_calls=[
            ChoiceDeltaToolCall(
                index=0, id='', 
                function=ChoiceDeltaToolCallFunction(arguments='{"path": "', name=None), type='function')
            ],
            reasoning_content=None), finish_reason=None, index=0, logprobs=None)
        Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None,
            tool_calls=[ChoiceDeltaToolCall(index=0, id='', function=ChoiceDeltaToolCallFunction(arguments='/home', name=None), type='function')], reasoning_content=None), finish_reason=None, index=0, logprobs=None)
        Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None,
            tool_calls=[ChoiceDeltaToolCall(index=0, id='', function=ChoiceDeltaToolCallFunction(arguments='/user/诗歌/', name=None), type='function')], reasoning_content=None), finish_reason=None, index=0, logprobs=None)
"""
        if choice.delta.tool_calls:
            tool_calls_chunk.extend(choice.delta.tool_calls)

        """
        reasoning_content在sdk的定义中是没有的，是openai的API增加的字段，因为API的更新会快，可能增加很多字段
        Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role='assistant',
               tool_calls=None, reasoning_content='用户'), finish_reason=None, index=0, logprobs=None)
        Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None,
               tool_calls=None, reasoning_content='要求我把'), finish_reason=None, index=0, logprobs=None)
        """
        reasoning_content = getattr(choice.delta, "reasoning_content", None)
        if reasoning_content:
            reasoning_content_chunk.append(reasoning_content)
            print(reasoning_content, end="")
        finish_reason = choice.finish_reason

    # 与block的区别，主要就在于参数的拼接。而且是拼接ChoiceDeltaToolCallFunction的parameter和name
    if finish_reason == "tool_calls":
        delta_tool_call = {}
        for tool_call in tool_calls_chunk:
            if tool_call.index not in delta_tool_call:
                delta_tool_call[tool_call.index] = {"name": tool_call.function.name, "arguments": tool_call.function.arguments}
            elif tool_call.function.name:
                delta_tool_call[tool_call.index]["name"] += tool_call.function.name
            elif tool_call.function.arguments:
                delta_tool_call[tool_call.index]["arguments"] += tool_call.function.arguments
        for index, tool_call in delta_tool_call.items():
            arguments = json.loads(tool_call["arguments"])
            print(arguments)
            if tool_call["name"] == "create_file":
                create_file(**arguments)


if __name__ == '__main__':
    # block_function_call()
    # block_function_call_2()
    stream_function_call()
