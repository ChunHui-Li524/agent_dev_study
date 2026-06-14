# AI Agent 学习工程 — 练习方案 v2

主线场景：**AI 专家 Agent**（开发过程中随时询问 AI 概念、API、框架知识）

## 学习方式

1. 阅读 `notes/` 与 `example/`（只读参考）
2. 在 `practice/` **闭卷手打**对应练习
3. 完成「必做变式」
4. 在 `PRACTICE_LOG.md` 勾选自检项

**practice 统一使用通义千问**：`DASHSCOPE_API_KEY` + `DASHSCOPE_BASE_URL`  
**example 使用 OpenAI 写法**，文件头注释说明如何改为通义。

## 版本演进

| 版本 | 阶段 | 能力 |
|------|------|------|
| v0 | Phase 1 初 | CLI 基础问答 |
| v1 | Phase 1 综合 | 流式 + Tool + 重试 |
| v2 | Phase 2 | LangChain Memory + Agent |
| v3 | Phase 3 | RAG 知识库检索 |
| v4 | Phase 4 | 多 Agent 协作 |
| v5 | Phase 5 | CrewAI 任务编排 |
| v6 | Phase 6 | PySide6 桌面 UI |
| v7 | Capstone | 可交付 AI 学习助手 |

## Phase 1：API 基础（4～6 周）

| # | example | practice | 变式 |
|---|---------|----------|------|
| 01 | `01_openai_basic.py` | `01_api.py` | AI 专家 persona ✅ |
| 02 | `02_openai_streaming.py` | `02_streaming.py` | 流式 + chunk 统计 |
| 03 | `03_error_retry.py` | `03_error_retry.py` | 封装 `call_llm()` |
| 04 | `04_token_usage.py` | `04_token_usage.py` | 打印 token 消耗 |
| 05 | `05_async_batch.py` | `05_async_batch.py` | 批量问 3 个 AI 概念 |
| 06 | `06_function_calling_basic.py` | `06_function_calling.py` | `lookup_glossary` |
| 07 | `07_function_calling_loop.py` | `07_tool_loop.py` | 多步 tool 循环 |
| 08 | `08_stream_tool_call.py` | `08_stream_tool.py` | 流式 tool 拼接 |
| 09 | `09_ai_expert_v1.py` | `09_ai_expert_v1.py` | **综合 v1** |

> 已有 `02_function_calling.py` 保留，内容可迁移至 06～08。

## Phase 2：LangChain（4～5 周）

| # | example | practice |
|---|---------|----------|
| 01 | `01_prompt_template.py` | `01_prompt_template.py` |
| 02 | `02_llm_chain.py` | `02_llm_chain.py` |
| 03 | `03_output_parser.py` | `03_output_parser.py` |
| 04 | `04_memory.py` | `04_memory.py` |
| 05 | `05_tools_langchain.py` | `05_tools.py` |
| 06 | `06_agent_react.py` | `06_agent.py` |
| 07 | `07_rag_langchain.py` | `07_rag_basic.py` |
| 08 | `08_ai_expert_v2.py` | `08_ai_expert_v2.py` |

## Phase 3：LlamaIndex / RAG（3～4 周）

| # | example | practice |
|---|---------|----------|
| 01 | `01_document_loader.py` | `01_document_loader.py` |
| 02 | `02_text_splitter.py` | `02_text_splitter.py` |
| 03 | `03_vector_index.py` | `03_vector_index.py` |
| 04 | `04_query_engine.py` | `04_query_engine.py` |
| 05 | `05_rag_with_citation.py` | `05_rag_citation.py` |
| 06 | `06_rag_eval.py` | `06_rag_eval.py` |
| 07 | `07_ai_expert_v3.py` | `07_ai_expert_v3.py` |

## Phase 4：AutoGen（2～3 周）

| # | example | practice |
|---|---------|----------|
| 01 | `01_basic_conversation.py` | `01_basic_conversation.py` |
| 02 | `02_two_agent_tutor.py` | `02_tutor_learner.py` |
| 03 | `03_group_chat.py` | `03_study_group.py` |
| 04 | `04_human_in_loop.py` | `04_human_in_loop.py` |
| 05 | `05_code_executor.py` | `05_code_demo.py` |
| 06 | `06_ai_study_panel.py` | `06_ai_study_panel.py` |

## Phase 5：CrewAI（2～3 周）

| # | example | practice |
|---|---------|----------|
| 01 | `01_basics.py` | `01_basics.py` |
| 02 | `02_researcher_writer.py` | `02_researcher_writer.py` |
| 03 | `03_ai_topic_crew.py` | `03_ai_topic_crew.py` |
| 04 | `04_crew_with_tools.py` | `04_crew_tools.py` |
| 05 | `05_hierarchical_crew.py` | `05_hierarchical.py` |
| 06 | `06_ai_content_pipeline.py` | `06_ai_content_pipeline.py` |

## Phase 6：PySide6 UI（3～4 周）

| # | example | practice |
|---|---------|----------|
| 01 | `01_pyside6_basics.py` | `01_pyside6_basics.py` |
| 02 | `02_chat_widget.py` | `02_chat_widget.py` |
| 03 | `03_thread_streaming.py` | `03_thread_streaming.py` |
| 04 | `04_integrate_llm.py` | `04_integrate_llm.py` |
| 05 | `05_integrate_rag.py` | `05_integrate_rag.py` |
| 06 | `06_settings_panel.py` | `06_settings_panel.py` |
| 07 | `07_packaging_notes.md` | 阅读 + 实践打包 |
| 选修 | `optional_fastapi_sse.py` | `optional_web_demo.py` |

## Capstone：AI 学习助手桌面版

目录：`capstone/ai_learning_assistant/`

PySide6 + 通义千问 + RAG + LangChain Agent，流式对话、知识库引用、工具调用。

## 参考

详细进度见 `PRACTICE_LOG.md`。
