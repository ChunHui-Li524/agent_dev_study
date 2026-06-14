"""
==========================================
示例 2: LangChain LCEL Chain
==========================================
学习目标：
1. 使用 LCEL（LangChain Expression Language）构建链
2. 组合 Prompt + LLM 实现 AI 导师
3. 链式调用与结构化输出
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0.7,
)


def build_tutor_chain():
    """构建 AI 导师 LCEL 链"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是 AI 技术导师，用简洁结构化的方式讲解概念。"),
        ("user", "主题: {topic}\n难度: {level}\n请给出：定义、要点、学习建议。"),
    ])
    return prompt | llm | StrOutputParser()


def run_chain(chain, topic, level="入门"):
    """执行链并打印结果"""

    print(f"=== 主题: {topic}（{level}）===\n")
    result = chain.invoke({"topic": topic, "level": level})
    print(result)
    print()


def batch_invoke(chain, topics):
    """批量调用链"""

    inputs = [{"topic": t, "level": "入门"} for t in topics]
    print("=== 批量调用 ===\n")
    for topic, result in zip(topics, chain.batch(inputs)):
        print(f"【{topic}】")
        print(result[:200] + "...\n")


def chain_with_config(chain):
    """带运行配置的链调用"""

    print("=== 低温度精确回答 ===\n")
    result = chain.invoke(
        {"topic": "向量数据库", "level": "进阶"},
        config={"configurable": {"temperature": 0.2}},
    )
    print(result)


if __name__ == "__main__":
    print("🚀 示例 2: LangChain LCEL Chain\n")

    tutor_chain = build_tutor_chain()
    run_chain(tutor_chain, "什么是 RAG")
    # batch_invoke(tutor_chain, ["Agent", "Function Calling"])
    # chain_with_config(tutor_chain)

    print("✅ 示例运行完成！")
