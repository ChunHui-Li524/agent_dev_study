"""
==========================================
示例 7: LangChain RAG
==========================================
学习目标：
1. 加载 data/ai_knowledge 文档
2. 文本切分、向量化与检索
3. 构建基础 RAG 问答链
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "data" / "ai_knowledge"


def load_documents():
    """加载知识库文档，不存在时使用内置示例"""

    if KNOWLEDGE_DIR.exists():
        loader = DirectoryLoader(
            str(KNOWLEDGE_DIR),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        docs = loader.load()
        print(f"=== 加载 {len(docs)} 个文档 ===\n")
        return docs

    from langchain.schema import Document
    print("注意: 未找到 data/ai_knowledge，使用内置文档\n")
    return [Document(page_content="RAG 是检索增强生成，结合向量检索与大模型。")]


def build_rag_chain():
    """构建 RAG 检索问答链"""

    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    splits = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = Chroma.from_documents(splits, embeddings)

    prompt = PromptTemplate(
        template="基于以下上下文回答问题。上下文:\n{context}\n\n问题: {question}",
        input_variables=["context", "question"],
    )
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0.3,
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt},
    )


def ask_questions(qa_chain):
    """提问示例"""

    questions = ["什么是 RAG？", "AI Agent 有哪些关键能力？"]
    for q in questions:
        print(f"=== 问题: {q} ===\n")
        answer = qa_chain.invoke({"query": q})
        print(answer["result"])
        print()


if __name__ == "__main__":
    print("🚀 示例 7: LangChain RAG\n")

    rag_chain = build_rag_chain()
    ask_questions(rag_chain)

    print("✅ 示例运行完成！")
