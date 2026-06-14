# 评分参考 — 各阶段练习要点

本文件供评卷时快速查阅。详细映射以 `LEARNING_PLAN.md` 为准。

## Phase 1 — API 基础

| # | practice | 核心能力 | 必做变式 |
|---|----------|----------|----------|
| 01 | `01_api.py` | Client 初始化、messages、create 调用 | AI 专家 persona |
| 02 | `02_streaming.py` | stream=True、遍历 chunk、delta.content 判空 | 流式 + chunk 统计与耗时 |
| 03 | `03_error_retry.py` | 封装 call_llm()、重试/退避 | 封装 call_llm() |
| 04 | `04_token_usage.py` | 读取 usage 字段 | 打印 token 消耗 |
| 05 | `05_async_batch.py` | AsyncOpenAI、asyncio.gather | 批量问 3 个 AI 概念 |
| 06 | `06_function_calling.py` | tools schema、tool_calls | lookup_glossary |
| 07 | `07_tool_loop.py` | 多轮 tool 消息回传、finish_reason 循环 | 多步 tool 循环 |
| 08 | `08_stream_tool.py` | 流式 tool_calls 拼接 | 流式 tool 拼接 |
| 09 | `09_ai_expert_v1.py` | CLI 交互、串联 ≥3 项能力 | 综合 v1 |

## Phase 2 — LangChain

| # | practice | 典型核心能力 |
|---|----------|--------------|
| 01 | `01_prompt_template.py` | PromptTemplate、变量填充 |
| 02 | `02_llm_chain.py` | LLMChain / LCEL 链式调用 |
| 03 | `03_output_parser.py` | 结构化输出解析 |
| 04 | `04_memory.py` | ConversationBufferMemory 等 |
| 05 | `05_tools.py` | LangChain Tool 定义与绑定 |
| 06 | `06_agent.py` | ReAct Agent 循环 |
| 07 | `07_rag_basic.py` | 文档加载 + 检索问答 |
| 08 | `08_ai_expert_v2.py` | Memory + Agent 综合 v2 |

## Phase 3 — LlamaIndex

| # | practice | 典型核心能力 |
|---|----------|--------------|
| 01～04 | 文档加载～QueryEngine | Loader、Splitter、Index、查询 |
| 05 | `05_rag_citation.py` | 引用来源 |
| 06 | `06_rag_eval.py` | RAG 评测指标 |
| 07 | `07_ai_expert_v3.py` | RAG 综合 v3 |

## Phase 4 — AutoGen

多 Agent 对话、Group Chat、Human-in-the-loop、代码执行；综合 `06_ai_study_panel.py`。

## Phase 5 — CrewAI

Agent/Role/Task/Crew 定义；层级 Crew；综合 `06_ai_content_pipeline.py`。

## Phase 6 — PySide6

Widget 布局、聊天 UI、QThread 流式、LLM/RAG 集成、设置面板；`07_packaging_notes.md` 为阅读+实践。

## Capstone

对照 `capstone/ai_learning_assistant/README.md`：
- 骨架：PySide6 + 通义 + 项目结构
- 核心：流式对话、RAG 引用、工具调用
- 交付：评测数据、README、可运行

## 综合练习额外标准

阶段末「综合」练习（v1/v2/v3 等）除单项能力外，检查：
- [ ] 可交互或可按场景演示
- [ ] 主线「AI 专家 Agent」场景一致
- [ ] 串联该阶段 ≥3 项已学能力
