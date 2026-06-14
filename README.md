# AI Agent 学习工程

从 API 基础到 PySide6 桌面应用的完整学习路径，主线场景为 **AI 专家 Agent**（开发过程中随时询问 AI 概念与框架知识）。

## 学习路线

| 阶段 | 内容 | 学习目标 | 状态 |
|------|------|----------|------|
| 1 | API 基础 | Chat Completions、流式、Tool Calling、重试 | 📝 进行中 |
| 2 | LangChain | Prompt、Chain、Memory、Agent、RAG | 📝 待开始 |
| 3 | LlamaIndex | 文档索引、向量检索、RAG 深入 | 📝 待开始 |
| 4 | AutoGen | 多智能体协作 | 📝 待开始 |
| 5 | CrewAI | 团队式 Agent 任务编排 | 📝 待开始 |
| 6 | PySide6 UI | 桌面聊天界面、线程流式、RAG 侧栏 | 📝 待开始 |
| Capstone | AI 学习助手 | 可交付桌面作品集 | 📝 待开始 |

## 学习方式

1. 阅读 `LEARNING_PLAN.md` 与 `notes/`
2. 参考 `example/`（只读，不修改）
3. 在 `practice/` **闭卷手打**代码
4. 在 `PRACTICE_LOG.md` 勾选进度

**practice 推荐使用通义千问**：`DASHSCOPE_API_KEY` + `DASHSCOPE_BASE_URL`

## 快速开始

```bash
cd d:/PythonProject/ai_agent
python -m venv venv
venv\Scripts\activate
copy .env.example .env
pip install -r requirements.txt
```

运行 Phase 1 示例：

```bash
cd phase1_api_basics
python example/01_openai_basic.py
```

## 目录结构

```
ai_agent/
├── LEARNING_PLAN.md           # 完整练习方案
├── PRACTICE_LOG.md            # 进度勾选
├── data/ai_knowledge/         # 共享 AI 知识库（RAG）
├── phase1_api_basics/         # API 基础
├── phase2_langchain/          # LangChain
├── phase3_llamaindex/         # LlamaIndex
├── phase4_autogen/            # AutoGen
├── phase5_crewai/             # CrewAI
├── phase6_ui/                 # PySide6 桌面 UI
└── capstone/
    └── ai_learning_assistant/ # 毕业项目
```

## LLM 配置

| 提供商 | 环境变量 |
|--------|----------|
| OpenAI（example） | `OPENAI_API_KEY` |
| 通义千问（practice） | `DASHSCOPE_API_KEY`, `DASHSCOPE_BASE_URL` |

## 参考资源

- [OpenAI API](https://platform.openai.com/docs)
- [LangChain](https://python.langchain.com)
- [LlamaIndex](https://docs.llamaindex.ai)
- [AutoGen](https://microsoft.github.io/autogen)
- [CrewAI](https://docs.crewai.com)
- [PySide6](https://doc.qt.io/qtforpython-6/)

---

**详细练习清单见 `LEARNING_PLAN.md`，开始你的 AI Agent 学习之旅吧！**
