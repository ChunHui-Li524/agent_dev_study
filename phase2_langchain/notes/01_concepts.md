# LangChain 核心概念笔记

## LangChain 是什么？

LangChain 是一个开发框架，用于构建由大语言模型驱动的应用。它提供了模块化的组件，可以轻松地组合成复杂的应用。

## 核心六大组件

### 1. Models（模型）

提供与各种 LLM 交互的统一接口。

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

response = llm.invoke("你好")
```

**支持的模型：**
- OpenAI (GPT 系列模型)
- Anthropic (Claude)
- 本地模型 (Ollama、Llama.cpp)

### 2. Prompts（提示）

管理提示的创建和格式化。

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手。"),
    ("user", "{input}")
])
```

**优势：**
- 提示和数据分离
- 可复用
- 支持变量插值
- 支持输出解析

### 3. Chains（链）

将多个组件串联起来执行。

```python
from langchain.chains import LLMChain

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

result = chain.invoke({"input": "你好"})
```

**常见 Chain 类型：**
- `LLMChain`: 最基础的链
- `SequentialChain`: 按顺序执行多个链
- `RouterChain`: 根据条件路由到不同的链

### 4. Memory（记忆）

在对话中保存和检索上下文。

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.save_context(
    {"input": "我叫张三"},
    {"output": "你好，张三！"}
)
```

**Memory 类型：**
- `ConversationBufferMemory`: 保存所有历史
- `ConversationBufferWindowMemory`: 只保存最近的 K 条
- `ConversationSummaryMemory`: 保存摘要
- `VectorStoreMemory`: 向量检索历史

### 5. Agents（智能体）

根据输入自动选择和使用工具。

```python
from langchain.agents import initialize_agent, Tool

agent = initialize_agent(
    tools=[],
    llm=llm,
    agent_type="zero-shot-react-description"
)
```

**Agent 工作流程：**
1. 接收用户输入
2. 决定是否需要使用工具
3. 选择并执行工具
4. 根据工具输出生成最终回复

### 6. Indexes（索引）

管理文档的存储和检索。

```python
from langchain.indexes import VectorStoreIndexCreator

index = VectorStoreIndexCreator()
index.from_documents(documents)
```

**核心组件：**
- Document Loaders: 加载文档
- Text Splitters: 分割文本
- Embeddings: 文本向量化
- Vector Stores: 向量存储和检索

## 提示工程最佳实践

### 1. System Prompt 要明确

```python
system_prompt = """
你是一个专业的 {role}。
请遵循以下规则：
1. 回答要简洁
2. 使用 {language}
3. 提供 {detail_level} 的细节
"""
```

### 2. 使用 Few-shot Learning

```python
examples = [
    {"input": "苹果", "output": "水果"},
    {"input": "胡萝卜", "output": "蔬菜"}
]
```

### 3. 添加约束条件

```python
prompt = """
请回答以下问题。
要求：
- 不超过 100 字
- 使用列表格式
- 包含至少 3 个要点
"""
```

## Chain 设计模式

### 1. 顺序链（Sequential Chain）

```python
from langchain.chains import SequentialChain

chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=["input"],
    output_variables=["final_output"]
)
```

### 2. 路由链（Router Chain）

```python
from langchain.chains import RouterChain

router = RouterChain(
    chains={
        "tech": tech_chain,
        "general": general_chain
    }
)
```

## Agent 类型

| Agent 类型 | 特点 | 适用场景 |
|------------|------|----------|
| Zero-shot | 无需示例，直接推理 | 简单任务 |
| ReAct | 思考-行动循环 | 复杂推理 |
| Self-Ask | 自问自答 | 多步推理 |
| Conversational | 带记忆的对话 | 对话应用 |

## 常见问题

### 1. LangChain vs 直接调用 API？

**LangChain 优势：**
- 模块化设计
- 丰富的预构建组件
- 社区支持

**直接调用 API 优势：**
- 更简单
- 更可控
- 更少的依赖

### 2. Memory 消耗太多 Token？

**解决方案：**
- 使用 `ConversationSummaryMemory` 保存摘要
- 使用 `ConversationBufferWindowMemory` 限制窗口
- 定期清理过期对话

### 3. Agent 卡住不输出？

**解决方案：**
- 调整 `max_iterations` 参数
- 优化 Tool 的描述
- 使用 `verbose=True` 调试

## 参考资源

- [LangChain 官方文档](https://python.langchain.com)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangChain CookBook](https://github.com/langchain-ai/langchain/tree/master/cookbook)
