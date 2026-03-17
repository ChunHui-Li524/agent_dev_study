"""
==========================================
示例 2: OpenAI 流式输出
==========================================
学习目标：
1. 如何使用流式输出（Streaming）
2. 实时显示生成内容
3. 处理流式响应的块（Chunk）
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def basic_streaming():
    """基础流式输出示例"""

    print("=== AI 正在生成（流式输出）===\n")

    # 调用 API，设置 stream=True
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "写一个关于 AI Agent 的短故事，大约 200 字。"}
        ],
        stream=True,  # 启用流式输出
        temperature=0.8
    )

    # 逐块接收和打印
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)  # 逐字显示
            full_response += content

    print("\n\n=== 生成完成 ===")
    print(f"总长度: {len(full_response)} 字符")


def streaming_with_metadata():
    """流式输出 + 显示元信息"""

    print("=== 带元信息的流式输出 ===\n")

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "解释 Python 的装饰器概念。"}
        ],
        stream=True,
        temperature=0.7
    )

    chunk_count = 0
    start_time = time.time()

    for chunk in stream:
        chunk_count += 1
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)

    elapsed_time = time.time() - start_time
    print(f"\n\n=== 统计 ===")
    print(f"总块数: {chunk_count}")
    print(f"耗时: {elapsed_time:.2f} 秒")
    print(f"平均每块耗时: {elapsed_time/chunk_count*1000:.2f} 毫秒")


def streaming_with_interrupt():
    """可中断的流式输出"""

    print("=== 流式输出（用户可中断）===\n")
    print("提示：按 Ctrl+C 可中断生成\n")

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "写一篇关于 AI 技术发展的文章。"}
        ],
        stream=True,
        temperature=0.7
    )

    try:
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
                # 这里可以添加中断逻辑
                # if some_condition:
                #     break

    except KeyboardInterrupt:
        print("\n\n=== 用户中断 ===")
        print("生成被用户中断")

    print("\n=== 完成 ===")


def streaming_for_code():
    """代码生成场景的流式输出"""

    print("=== 代码生成（流式输出）===\n")

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个编程专家，提供带注释的代码。"},
            {"role": "user", "content": "用 Python 写一个快速排序算法。"}
        ],
        stream=True,
        temperature=0.3  # 代码生成建议使用较低温度
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)


def streaming_with_typing_effect():
    """打字机效果的流式输出"""

    print("=== 打字机效果 ===\n")

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "用诗意的语言描述夕阳。"}
        ],
        stream=True,
        temperature=0.9
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            # 短暂延迟，模拟打字效果
            time.sleep(0.02)


if __name__ == "__main__":
    print("🚀 示例 2: OpenAI 流式输出\n")

    # 运行各个示例
    # basic_streaming()
    # streaming_with_metadata()
    # streaming_with_interrupt()
    # streaming_for_code()
    streaming_with_typing_effect()

    print("\n✅ 示例运行完成！")
