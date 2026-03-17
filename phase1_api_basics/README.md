# Phase 1: API 基础

学习如何直接调用大语言模型 API，这是构建 AI Agent 的第一步。

## 学习目标

完成本阶段后，你将能够：

- ✅ 调用 OpenAI API（GPT 系列模型）
- ✅ 调用 Anthropic API（Claude 模型）
- ✅ 调用国内模型 API（智谱、通义千问、文心一言）
- ✅ 处理流式输出（Streaming）
- ✅ 使用异步调用提高效率
- ✅ 处理 API 错误和重试机制
- ✅ 管理 Token 使用量

## 前置条件

1. 已创建并激活虚拟环境
2. 已在项目根目录配置 `.env` 文件
3. 已安装阶段依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 目录结构

```
phase1_api_basics/
├── example/               # AI 生成的示例代码（带注释和说明）
│   ├── 01_openai_basic.py           # OpenAI 基础调用
│   ├── 02_openai_streaming.py       # OpenAI 流式输出
│   ├── 03_anthropic_basic.py        # Anthropic 基础调用
│   ├── 04_zhipuai_basic.py          # 智谱 AI 调用
│   ├── 05_dashscope_basic.py        # 通义千问调用
│   ├── 06_qianfan_basic.py          # 文心一言调用
│   ├── 07_async_request.py          # 异步调用示例
│   ├── 08_error_handling.py         # 错误处理与重试
│   └── 09_token_management.py       # Token 管理
├── practice/              # 手动练习代码（初始为空）
│   ├── __init__.py
│   └── .gitkeep
├── notes/                 # 学习笔记
│   ├── 01_openai_api.md
│   ├── 02_anthropic_api.md
│   ├── 03_domestic_llm.md
│   └── 04_best_practices.md
├── tests/                 # 测试文件
│   ├── __init__.py
│   ├── test_openai_api.py
│   └── test_anthropic_api.py
├── config/                # 配置文件
│   ├── model_configs.json
│   └── .env.example
└── requirements.txt       # 本阶段依赖
```

## 学习路径

### 第 1 步：OpenAI API 基础

**示例代码：** `example/01_openai_basic.py`

**学习重点：**
- 使用 OpenAI SDK 进行基础调用
- 理解 Chat Completion API 参数
- 处理响应数据

**练习任务：**
- 在 `practice/` 目录手动敲一遍代码
- 尝试不同的模型（gpt-4、gpt-4o、gpt-4o-mini）
- 调整 temperature 和 max_tokens 参数

### 第 2 步：流式输出

**示例代码：** `example/02_openai_streaming.py`

**学习重点：**
- 流式输出原理
- SSE (Server-Sent Events) 处理
- 实时显示生成内容

### 第 3 步：Anthropic API

**示例代码：** `example/03_anthropic_basic.py`

**学习重点：**
- Anthropic SDK 使用方法
- Claude 模型特性
- Message API 格式

### 第 4 步：国内模型 API

**示例代码：**
- `example/04_zhipuai_basic.py` - 智谱 AI
- `example/05_dashscope_basic.py` - 通义千问
- `example/06_qianfan_basic.py` - 文心一言

**学习重点：**
- 各家 API 的差异
- 接口封装方法
- 模型选择策略

### 第 5 步：异步调用

**示例代码：** `example/07_async_request.py`

**学习重点：**
- async/await 语法
- aiohttp 异步请求
- 并发批量处理

### 第 6 步：错误处理

**示例代码：** `example/08_error_handling.py`

**学习重点：**
- 常见错误类型
- 重试策略（指数退避）
- 降级方案

### 第 7 步：Token 管理

**示例代码：** `example/09_token_management.py`

**学习重点：**
- Token 计算方法
- 成本估算
- 优化策略

## 运行示例

```bash
# 进入阶段目录
cd phase1_api_basics

# 运行特定示例
python example/01_openai_basic.py

# 运行所有测试
pytest tests/
```

## 配置说明

在 `config/model_configs.json` 中预定义了各模型的参数：

```json
{
  "openai": {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "anthropic": {
    "model": "claude-3-sonnet-20240229",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

## 常见问题

### 1. API 调用失败，提示认证错误

- 检查 `.env` 文件中 API Key 是否正确
- 确认 API Key 是否有足够额度

### 2. 如何降低 API 费用？

- 使用更便宜的模型（如 gpt-4o-mini 替代 gpt-4）
- 减少上下文长度
- 批量处理请求

### 3. 国内模型是否需要代理？

- 智谱、通义千问、文心一言：无需代理
- OpenAI、Anthropic：可能需要配置代理

## 下一步

完成本阶段后，进入 **Phase 2: LangChain**，学习如何使用 LangChain 框架构建更复杂的 AI Agent。

---

**开始学习吧！** 📚
