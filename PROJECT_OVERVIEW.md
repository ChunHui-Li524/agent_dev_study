# AI Agent 学习工程 — 项目概览

> 完整练习方案见 [LEARNING_PLAN.md](LEARNING_PLAN.md)，进度见 [PRACTICE_LOG.md](PRACTICE_LOG.md)

## 主线场景

**AI 专家 Agent**：面向开发者的 AI 技术学习助手，贯穿 5 个框架阶段 + PySide6 UI + 毕业项目。

## 阶段与文件统计

| 阶段 | example 数 | practice 数 | 综合项目 |
|------|------------|-------------|----------|
| Phase 1 API | 9 | 9 + 1 进阶 | `09_ai_expert_v1.py` |
| Phase 2 LangChain | 8 | 8 | `08_ai_expert_v2.py` |
| Phase 3 LlamaIndex | 7 | 7 | `07_ai_expert_v3.py` |
| Phase 4 AutoGen | 6 | 6 | `06_ai_study_panel.py` |
| Phase 5 CrewAI | 6 | 6 | `06_ai_content_pipeline.py` |
| Phase 6 PySide6 | 7 + 1 选修 | 7 | — |
| Capstone | — | — | `ai_learning_assistant/` |

## 目录结构

```
ai_agent/
├── LEARNING_PLAN.md
├── PRACTICE_LOG.md
├── README.md
├── requirements.txt
├── data/ai_knowledge/              # 共享 RAG 知识库
│
├── phase1_api_basics/
│   ├── example/     01～09
│   ├── practice/    手打练习
│   ├── notes/
│   ├── checklist/
│   └── data/ai_knowledge/
│
├── phase2_langchain/    example 01～08, practice
├── phase3_llamaindex/   example 01～07, practice
├── phase4_autogen/      example 01～06, practice
├── phase5_crewai/       example 01～06, practice
│
├── phase6_ui/           PySide6 桌面 UI
│   ├── example/         01～06 + packaging + FastAPI 选修
│   ├── practice/
│   └── notes/
│
└── capstone/ai_learning_assistant/
    ├── app/             PySide6 + Agent + RAG
    ├── data/
    ├── eval/
    └── tests/
```

## 版本演进

| 版本 | 能力 |
|------|------|
| v1 | CLI：流式 + Tool + 重试（Phase 1） |
| v2 | LangChain Memory + Agent（Phase 2） |
| v3 | RAG 知识库检索（Phase 3） |
| v4 | 多 Agent 协作（Phase 4～5） |
| v5 | PySide6 桌面应用（Phase 6） |
| v6 | Capstone 可交付作品 |

## 快速开始

```bash
pip install -r requirements.txt
copy .env.example .env
cd phase1_api_basics && python example/01_openai_basic.py
```

## 毕业项目

`capstone/ai_learning_assistant/` — PySide6 + 通义千问 + RAG + LangChain Agent 桌面 AI 学习助手。

```bash
cd capstone/ai_learning_assistant
pip install -r requirements.txt
python -m app.main
```
