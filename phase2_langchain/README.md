# Phase 2: LangChain

学习 LangChain 框架，构建更复杂的 AI Agent 和应用。

## 学习目标

完成本阶段后，你将能够：

- ✅ 理解 LangChain 的核心概念（Chain、Prompt Template、Memory）
- ✅ 使用 Prompt Template 构建可复用的提示
- ✅ 实现 Chain 链式调用
- ✅ 使用 Memory 记住对话历史
- ✅ 创建 Agent 并集成 Tools
- ✅ 使用 Document Loaders 处理各种文件
- ✅ 实现基础的 RAG（检索增强生成）

## 前置条件

1. ✅ 已完成 Phase 1（API 基础）
2. 已在项目根目录配置 `.env` 文件
3. 已安装阶段依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 目录结构

```
phase2_langchain/
├── example/               # AI 生成的示例代码
│   ├── 01_prompt_template.py          # Prompt Template 基础
│   ├── 02_simple_chain.py             # Simple Chain 链式调用
│   ├── 03_sequence_chain.py           # Sequence Chain 顺序链
│   ├── 04_memory_conversation.py     # Memory 对话记忆
│   ├── 05_agent_basic.py              # Agent 基础
│   ├── 06_agent_with_tools.py         # Agent + Tools
│   ├── 07_document_loader.py         # 文档加载
│   ├── 08_vector_store.py             # 向量存储
│   └── 09_rag_basic.py                # RAG 基础
├── practice/              # 手动练习代码
├── notes/                 # 学习笔记
│   ├── 01_concepts.md
│   ├── 02_chains.md
│   ├── 03_memory.md
│   ├── 04_agents.md
│   └── 05_rag.md
├── tests/                 # 测试文件
├── config/                # 配置文件
└── requirements.txt       # 本阶段依赖
```

## LangChain 核心概念

### 1. Prompt Template（提示模板）

将提示的结构与数据分离，实现可复用。

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 {role}。"),
    ("user", "{question}")
])
```

### 2. Chain（链）

将多个组件串联起来执行。

```python
from langchain.chains import LLMChain

chain = LLMChain(
    llm=llm,
    prompt=prompt
)
```

### 3. Memory（记忆）

在对话中保存和检索上下文。

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
```

### 4. Agent（智能体）

根据输入自动选择和使用工具。

```python
from langchain.agents import initialize_agent, Tool

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="zero-shot-react-description"
)
```

## 学习路径

### 第 1 步：Prompt Template

**示例代码：** `example/01_prompt_template.py`

**学习重点：**
- StringPromptTemplate 和 ChatPromptTemplate
- Few-shot Prompting
- 输出解析器（Output Parser）

### 第 2 步：Chains

**示例代码：** `example/02_simple_chain.py`、`example/03_sequence_chain.py`

**学习重点：**
- LLMChain
- SequentialChain
- RouterChain

### 第 3 步：Memory

**示例代码：** `example/04_memory_conversation.py`

**学习重点：**
- ConversationBufferMemory
- ConversationBufferWindowMemory
- ConversationSummaryMemory

### 第 4 步：Agents

**示例代码：** `example/05_agent_basic.py`、`example/06_agent_with_tools.py`

**学习重点：**
- Agent 工作原理
- ReAct Agent
- 自定义 Tools

### 第 5 步：Document Loaders

**示例代码：** `example/07_document_loader.py`

**学习重点：**
- 加载各种格式文件（PDF、TXT、HTML）
- Text Splter 分段
- 向量化

### 第 6 步：Vector Stores & RAG

**示例代码：** `example/08_vector_store.py`、`example/09_rag_basic.py`

**学习重点：**
- 向量存储（Chroma、FAISS）
- 相似度搜索
- RAG 实现原理

## 运行示例

```bash
# 进入阶段目录
cd phase2_langchain

# 运行特定示例
python example/01_prompt_template.py

# 运行所有测试
pytest tests/
```

## 常见问题

### 1. LangChain API 变动很快？

LangChain 更新频繁，建议关注官方文档和版本说明。

### 2. Agent 反复循环？

调整 Agent 的 max_iterations 参数，或优化 Tool 的描述。

### 3. Memory 消耗太多 Token？

使用 ConversationSummaryMemory 或限制窗口大小。

## 下一步

完成本阶段后，进入 **Phase 3: LlamaIndex**，深入学习数据索引和 RAG 技术。

---

**开始学习吧！** 🔗
