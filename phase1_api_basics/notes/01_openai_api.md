# OpenAI API 学习笔记

## 核心概念

### Chat Completion API

OpenAI 的 Chat Completion API 是调用大语言模型的主要接口。

```python
client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=0.7,
    max_tokens=1000
)
```

### 关键参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `model` | 模型选择 | `gpt-4o-mini`（性价比最高） |
| `messages` | 对话历史 | 数组格式，包含 role 和 content |
| `temperature` | 控制随机性 | 0.0-1.0，0.7 是平衡值 |
| `max_tokens` | 最大输出长度 | 根据需求设置 |
| `top_p` | 核采样 | 0.1-1.0，通常不设置 |
| `frequency_penalty` | 频率惩罚 | -2.0 到 2.0 |
| `presence_penalty` | 存在惩罚 | -2.0 到 2.0 |

### Messages 格式

```python
messages = [
    {"role": "system", "content": "你是一个有帮助的助手。"},
    {"role": "user", "content": "你好！"},
    {"role": "assistant", "content": "你好！有什么可以帮你？"},
    {"role": "user", "content": "解释什么是 AI。"}
]
```

**Role 类型：**
- `system`: 设置助手的行为和角色
- `user`: 用户的输入
- `assistant`: AI 的回复（在多轮对话中需要提供）

## 模型对比

| 模型 | 能力 | 输入成本 | 输出成本 | 推荐场景 |
|------|------|----------|----------|----------|
| GPT-4o | 最新最强 | $5/1M | $15/1M | 复杂任务、代码生成 |
| GPT-4o-mini | 高性价比 | $0.15/1M | $0.60/1M | 日常对话、简单任务 |
| GPT-3.5-turbo | 最便宜 | $0.50/1M | $1.50/1M | 简单分类、文本生成 |

## Token 管理

### Token 是什么？

- Token 是 API 计费的最小单位
- 1 Token ≈ 0.75 个英文单词 或 0.5-1 个汉字
- GPT-4o-mini 最大支持 128K tokens

### 计算方法

```python
import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")
text = "Hello, world!"
tokens = encoding.encode(text)
print(f"Token 数: {len(tokens)}")
```

### 节省成本的技巧

1. 使用更便宜的模型
2. 减少 System Prompt 长度
3. 限制 `max_tokens`
4. 批量处理请求
5. 使用流式输出提前终止

## 常见错误

### 1. 认证错误

```
Error: Incorrect API key provided
```

**解决方案：** 检查 `.env` 文件中的 `OPENAI_API_KEY`

### 2. 速率限制

```
Error: Rate limit exceeded
```

**解决方案：**
- 增加请求间隔
- 使用更便宜的模型（有更高的速率限制）
- 使用重试机制

### 3. 上下文超限

```
Error: This model's maximum context length is 128000 tokens
```

**解决方案：**
- 减少 messages 历史长度
- 使用支持更大上下文的模型
- 实现 RAG（检索增强生成）

## 最佳实践

1. **总是设置 temperature**
   - 创意任务：0.7-1.0
   - 代码生成：0.2-0.5
   - 事实回答：0.0-0.2

2. **合理的 System Prompt**
   - 明确角色定位
   - 提供清晰的输出格式
   - 设置边界条件

3. **处理多轮对话**
   - 保存完整的对话历史
   - 定期清理过时的对话
   - 使用总结压缩上下文

4. **错误处理**
   - 捕获所有异常
   - 实现指数退避重试
   - 记录错误日志

## 参考资源

- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [OpenAI Playground](https://platform.openai.com/playground) - 可视化测试
- [定价页面](https://openai.com/pricing)
