# Phase 1 练习自检清单

每项练习完成后勾选。

## 01 基础调用

- [x] 能闭卷写出 client 初始化与 create 调用
- [x] 能解释 system / user / assistant 角色
- [x] 变式：AI 专家 persona

## 02 流式输出

- [x] 能设置 stream=True 并遍历 chunk
- [x] 能处理 delta.content 为 None
- [x] 变式：统计 chunk 数与耗时

## 03 错误重试

- [x] 能封装 call_llm() 并指数退避
- [x] 能说明 401/429/timeout 处理思路

## 04 Token

- [x] 能读取 usage 字段
- [x] 变式：多轮累计 token

## 05 异步

- [x] 能使用 AsyncOpenAI + asyncio.gather

## 06～08 Function Calling

- [x] 能定义 tools schema
- [x] 能处理 tool_calls 并回传 tool 消息
- [x] 能根据 finish_reason 循环
- [ ] 能拼接流式 tool_calls

## 09 综合 v1

- [ ] CLI 可交互运行
- [ ] 串联流式/工具/重试/token 中至少 3 项