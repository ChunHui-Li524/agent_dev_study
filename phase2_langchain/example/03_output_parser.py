"""
==========================================
示例 3: LangChain Output Parser
==========================================
学习目标：
1. 使用 Pydantic 定义结构化输出
2. PydanticOutputParser 解析 LLM 回复
3. 为 AI 概念讲解生成标准格式
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0.5,
)


class ConceptExplanation(BaseModel):
    """AI 概念结构化讲解"""

    concept: str = Field(description="概念名称")
    definition: str = Field(description="一句话定义")
    explanation: str = Field(description="详细解释，100字左右")
    example: str = Field(description="实际应用示例")
    further_reading: list[str] = Field(description="延伸阅读关键词，2-3个")


def build_parser_chain():
    """构建带 Pydantic 解析器的链"""

    parser = PydanticOutputParser(pydantic_object=ConceptExplanation)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是 AI 教育专家，按指定格式讲解概念。\n{format_instructions}"),
        ("user", "请讲解概念: {concept}"),
    ])
    chain = prompt | llm | parser
    return chain, parser


def explain_concept(chain, concept):
    """讲解单个概念并打印结构化结果"""

    print(f"=== 概念: {concept} ===\n")
    result = chain.invoke({"concept": concept})
    print(f"定义: {result.definition}")
    print(f"解释: {result.explanation}")
    print(f"示例: {result.example}")
    print(f"延伸阅读: {', '.join(result.further_reading)}\n")
    return result


def explain_multiple(chain, concepts):
    """批量讲解多个概念"""

    print("=== 批量结构化讲解 ===\n")
    for concept in concepts:
        explain_concept(chain, concept)


if __name__ == "__main__":
    print("🚀 示例 3: LangChain Output Parser\n")

    parser_chain, _ = build_parser_chain()
    explain_concept(parser_chain, "RAG")
    # explain_multiple(parser_chain, ["Agent", "Embedding"])

    print("✅ 示例运行完成！")
