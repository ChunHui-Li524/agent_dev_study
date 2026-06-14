# AI Learning Assistant

基于 PySide6 的桌面 AI 学习助手，集成 DashScope/Qwen、RAG 与 LangChain，帮助用户系统学习 AI 概念。

## 项目概述

本应用提供对话式学习体验：用户提问，助手结合本地知识库（RAG）与工具调用（术语查询、主题推荐）给出结构化回答，并在侧边栏展示引用来源。

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                    MainWindow (PySide6)                  │
│  ┌──────────────────────┐  ┌──────────────────────────┐ │
│  │     ChatPanel        │  │      SourcePanel         │ │
│  │  (输入 / 对话展示)    │  │  (RAG 引用来源列表)       │ │
│  └──────────┬───────────┘  └────────────▲─────────────┘ │
└─────────────┼────────────────────────────┼────────────────┘
              │                            │
              ▼                            │
       ┌──────────────┐              ┌─────┴─────┐
       │ ExpertAgent  │──────────────│ Retriever │
       │ (LangChain)  │              │ (RAG)     │
       └──────┬───────┘              └─────▲─────┘
              │                          │
              ▼                          │
       ┌──────────────┐            data/ai_knowledge/
       │  llm_client  │            (ChromaDB + LlamaIndex)
       │  (DashScope) │
       └──────────────┘
```

**技术栈**

| 层级 | 技术 |
|------|------|
| UI | PySide6 |
| LLM | DashScope OpenAI 兼容接口 / Qwen |
| Agent | LangChain |
| RAG | LlamaIndex + ChromaDB |
| 配置 | python-dotenv + QSettings |

## 目录结构

```
ai_learning_assistant/
├── app/
│   ├── main.py              # 应用入口
│   ├── core/                # 配置、LLM 客户端
│   ├── ui/                  # 主窗口与面板
│   ├── agent/               # ExpertAgent 与工具
│   └── rag/                 # 检索器
├── data/ai_knowledge/       # 本地知识文档
├── eval/                    # QA 基准评测
├── tests/
└── requirements.txt
```

## 快速开始

```bash
cd capstone/ai_learning_assistant
pip install -r requirements.txt
cp ../../.env.example .env   # 填入 DASHSCOPE_API_KEY
python -m app.main
```

## 交付物清单

- [ ] 可运行的 PySide6 桌面应用（主窗口 + 聊天 + 来源面板）
- [ ] DashScope/Qwen LLM 集成（流式或非流式对话）
- [ ] RAG 检索：加载 `data/ai_knowledge/`，回答时展示引用
- [ ] LangChain Agent：`lookup_glossary`、`recommend_topic` 工具
- [ ] 配置持久化：环境变量 + QSettings（窗口尺寸、模型名等）
- [ ] `eval/qa_benchmark.json` 评测脚本或手动评测记录
- [ ] 单元测试通过：`pytest tests/`

## 简历一句话

> 独立开发 PySide6 桌面 AI 学习助手，集成通义千问、LangChain Agent 与 LlamaIndex RAG，实现对话式答疑、术语查询与知识引用展示。
