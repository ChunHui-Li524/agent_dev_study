"""
==========================================
示例 5: LangChain Tools
==========================================
学习目标：
1. 使用 @tool 装饰器定义工具
2. 实现 lookup_glossary 和 recommend_topic
3. 理解工具描述对模型选工具的影响
"""

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

GLOSSARY = {
    "RAG": "检索增强生成：先检索知识库再生成回答。",
    "Agent": "能调用工具、多步推理完成目标的 LLM 应用。",
    "Embedding": "将文本映射为向量，用于语义检索。",
}

TOPIC_PATH = {
    "RAG": "Phase 3 LlamaIndex - 向量索引与查询引擎",
    "Agent": "Phase 4 AutoGen - 多 Agent 协作",
    "Function Calling": "Phase 1 API 基础 - Tool 调用循环",
}


@tool
def lookup_glossary(term: str) -> str:
    """查询 AI 术语的定义，输入术语名称如 RAG、Agent。"""

    return GLOSSARY.get(term, f"未找到术语: {term}")


@tool
def recommend_topic(interest: str) -> str:
    """根据用户兴趣推荐下一个学习主题，输入兴趣关键词。"""

    for key, path in TOPIC_PATH.items():
        if key.lower() in interest.lower() or interest.lower() in key.lower():
            return f"推荐学习: {key} → {path}"
    return "推荐从 Phase 1 Function Calling 开始，再学 Agent 与 RAG。"


def demo_tools_directly():
    """直接调用工具（不经过 Agent）"""

    print("=== 直接调用工具 ===\n")
    print(f"lookup_glossary('RAG'): {lookup_glossary.invoke('RAG')}")
    print(f"recommend_topic('Agent'): {recommend_topic.invoke('Agent')}\n")


def demo_llm_with_tools():
    """让 LLM 绑定工具并选择调用"""

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0,
    )
    tools = [lookup_glossary, recommend_topic]
    llm_with_tools = llm.bind_tools(tools)

    print("=== LLM 选择工具 ===\n")
    response = llm_with_tools.invoke("请查一下 RAG 是什么意思，并推荐相关学习路径。")
    if response.tool_calls:
        for call in response.tool_calls:
            print(f"工具: {call['name']}, 参数: {call['args']}")
    else:
        print(response.content)


if __name__ == "__main__":
    print("🚀 示例 5: LangChain Tools\n")

    demo_tools_directly()
    demo_llm_with_tools()

    print("\n✅ 示例运行完成！")
