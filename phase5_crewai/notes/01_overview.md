# CrewAI 概览笔记

## CrewAI 是什么？

CrewAI 是一个专注于**团队式智能体协作**的框架，让你能够轻松创建由多个 AI Agent 组成的团队，协作完成复杂任务。

## 核心理念

```
Human (你)
    ↓
定义角色和任务
    ↓
┌─────────────────────────────┐
│         Crew (团队)         │
│  ┌─────┐  ┌─────┐  ┌─────┐  │
│  │Agent│  │Agent│  │Agent│  │
│  │  1  │  │  2  │  │  3  │  │
│  └─────┘  └─────┘  └─────┘  │
│       ↓        ↓        ↓   │
│    ┌─────────────────────┐  │
│    │   Tasks (任务)      │  │
│    └─────────────────────┘  │
└─────────────────────────────┘
    ↓
最终输出
```

## 三大核心组件

### 1. Agent（智能体）

具有角色、目标和背景故事的工作者。

```python
from crewai import Agent

agent = Agent(
    role="Python 研发工程师",
    goal="编写高质量的 Python 代码",
    backstory="你是一名资深 Python 开发者，有 8 年经验..."
)
```

**关键属性：**
- `role`: 角色（身份）
- `goal`: 目标（要做什么）
- `backstory`: 背景故事（性格、经验）
- `verbose`: 是否显示详细日志
- `llm`: 使用的 LLM 模型
- `tools`: 可用的工具
- `max_iter`: 最大迭代次数

### 2. Task（任务）

需要完成的具体工作。

```python
from crewai import Task

task = Task(
    description="编写一个快速排序算法",
    expected_output="Python 代码文件",
    agent=agent
)
```

**关键属性：**
- `description`: 任务描述
- `expected_output`: 期望的输出格式
- `agent`: 负责的 Agent
- `context`: 依赖的其他任务（上下文）

### 3. Crew（团队）

由多个 Agent 和 Task 组成的工作团队。

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential
)
```

**关键属性：**
- `agents`: Agent 列表
- `tasks`: Task 列表
- `process`: 执行流程
- `verbose`: 是否显示详细日志
- `memory`: 是否启用记忆
- `max_rpm`: 每分钟最大请求次数

## 执行流程（Process）

### 1. Sequential Process（顺序流程）

任务按顺序一个接一个执行。

```
Task1 → Task2 → Task3 → Task4 → 完成
```

**适用场景：**
- 线性工作流
- 任务有明确依赖
- 简单流程

**示例：**
```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential
)
```

### 2. Hierarchical Process（层级流程）

有一个 Manager Agent 协调其他 Agent。

```
        Manager
         /  |  \
        /   |   \
     Task1 Task2 Task3
```

**适用场景：**
- 复杂多任务
- 需要动态分配
- 并行处理

**示例：**
```python
crew = Crew(
    agents=[manager, agent1, agent2],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_llm="gpt-4"
)
```

## 工作流程

### 典型流程

```
1. 定义需求
   ↓
2. 创建 Agent（角色、目标、背景）
   ↓
3. 定义 Task（描述、输出、负责人）
   ↓
4. 组装 Crew（Agent + Task + Process）
   ↓
5. 执行（kickoff）
   ↓
6. 获取结果
```

### 代码示例

```python
# 1. 定义 Agent
researcher = Agent(
    role="研究员",
    goal="研究技术趋势",
    backstory="你是资深研究员..."
)

# 2. 定义 Task
task = Task(
    description="研究 AI Agent 技术",
    expected_output="研究报告",
    agent=researcher
)

# 3. 组装 Crew
crew = Crew(
    agents=[researcher],
    tasks=[task],
    process=Process.sequential
)

# 4. 执行
result = crew.kickoff()
```

## 核心概念对比

| 概念 | 类比 | 作用 |
|------|------|------|
| Agent | 员工 | 具有特定能力的执行者 |
| Task | 工作任务 | 需要完成的具体工作 |
| Crew | 项目组 | 多个人协作完成多个任务 |
| Process | 工作流程 | 任务执行的顺序和方式 |

## CrewAI vs AutoGen vs LangChain

### CrewAI

**优势：**
- 专注团队协作
- Agent 角色化清晰
- 流程控制简单
- 工具集成丰富

**劣势：**
- 灵活性相对较低
- 对话能力较弱

### AutoGen

**优势：**
- 灵活的对话机制
- 支持复杂交互
- 代码执行能力强

**劣势：**
- 学习曲线较陡
- 不易控制

### LangChain

**优势：**
- 应用框架完整
- 组件丰富
- 社区活跃

**劣势：**
- 对多 Agent 支持较弱
- 团队协作能力有限

## 使用建议

### 什么时候用 CrewAI？

✅ 需要多角色协作
✅ 任务流程清晰
✅ 需要工具集成
✅ 希望简单易用

### 什么时候用 AutoGen？

✅ 需要灵活对话
✅ 复杂交互场景
✅ 需要代码执行
✅ 愿意投入更多学习时间

### 什么时候用 LangChain？

✅ 构建 LLM 应用
✅ 需要完整工具链
✅ RAG 应用
✅ 简单单 Agent 场景

## 参考资源

- [CrewAI 官方文档](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)
- [CrewAI Examples](https://github.com/joaomdmoura/crewAI-examples)
