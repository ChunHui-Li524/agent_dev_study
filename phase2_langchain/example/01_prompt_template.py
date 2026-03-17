"""
==========================================
示例 1: LangChain Prompt Template
==========================================
学习目标：
1. 使用 ChatPromptTemplate 创建可复用的提示
2. Few-shot Prompting（少样本学习）
3. 使用 Output Parser 解析输出
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0.7
)


def basic_template():
    """基础 Prompt Template"""

    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个 {role}。"),
        ("user", "{question}")
    ])

    # 格式化提示
    formatted_prompt = prompt.format(
        role="Python 编程专家",
        question="解释什么是装饰器"
    )

    print("=== 格式化后的提示 ===")
    print(formatted_prompt)
    print()

    # 调用 LLM
    response = llm.invoke(formatted_prompt)

    print("=== AI 回复 ===")
    print(response.content)


def few_shot_prompting():
    """Few-shot Prompting（少样本学习）"""

    # 示例数据
    examples = [
        {
            "question": "苹果是什么？",
            "answer": "苹果是一种水果，通常是红色或绿色的。"
        },
        {
            "question": "香蕉是什么？",
            "answer": "香蕉是一种黄色的热带水果。"
        }
    ]

    # 创建 Few-shot 模板
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=PromptTemplate(
            input_variables=["question", "answer"],
            template="问题: {question}\n答案: {answer}\n"
        ),
        prefix="以下是几个例子：",
        suffix="问题: {input}\n答案:",
        input_variables=["input"]
    )

    # 格式化提示
    formatted_prompt = prompt.format(input="西瓜是什么？")

    print("=== Few-shot 提示 ===")
    print(formatted_prompt)
    print()

    # 调用 LLM
    response = llm.invoke(formatted_prompt)

    print("=== AI 回复 ===")
    print(response.content)


def output_parser():
    """使用 Output Parser 解析输出"""

    # 创建输出解析器
    parser = CommaSeparatedListOutputParser()

    # 获取格式化说明
    format_instructions = parser.get_format_instructions()

    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个善于列出事项的助手。"),
        ("user", "{question}\n{format_instructions}")
    ])

    # 格式化提示
    formatted_prompt = prompt.format(
        question="列出 5 种流行的编程语言。",
        format_instructions=format_instructions
    )

    print("=== 提示 ===")
    print(formatted_prompt)
    print()

    # 调用 LLM
    response = llm.invoke(formatted_prompt)

    print("=== 原始输出 ===")
    print(response.content)
    print()

    # 解析输出
    parsed_output = parser.parse(response.content)

    print("=== 解析后的列表 ===")
    for i, item in enumerate(parsed_output, 1):
        print(f"{i}. {item}")


def structured_prompt():
    """结构化提示模板"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个 {expertise}，使用 {tone} 的语气。"),
        ("user", "{topic} 的定义是什么？"),
        ("user", "请提供一个 {style} 的例子。")
    ])

    formatted_prompt = prompt.format(
        expertise="计算机科学教授",
        tone="专业且易懂",
        topic="算法",
        style="简单"
    )

    print("=== 格式化后的提示 ===")
    print(formatted_prompt)
    print()

    response = llm.invoke(formatted_prompt)

    print("=== AI 回复 ===")
    print(response.content)


if __name__ == "__main__":
    print("🚀 示例 1: LangChain Prompt Template\n")

    # 运行各个示例
    # basic_template()
    # few_shot_prompting()
    # output_parser()
    structured_prompt()

    print("\n✅ 示例运行完成！")
