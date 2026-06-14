# Function Calling 简介

Function Calling（工具调用）让 LLM 输出结构化的工具请求，由应用程序执行后把结果回传给模型。

## 流程

1. 定义 tools（名称、描述、JSON Schema 参数）
2. 用户提问，模型返回 tool_calls 或文本
3. 程序执行工具，追加 role=tool 消息
4. 再次请求模型，生成最终回答

## 与 Agent 的关系

Function Calling 是 Agent「行动」环节的基础能力；多轮 tool 循环即简单 Agent。

## 注意事项

- parameters 需符合 JSON Schema
- 流式模式下 tool_calls 需增量拼接
- 通义/OpenAI 兼容接口字段可能略有差异
