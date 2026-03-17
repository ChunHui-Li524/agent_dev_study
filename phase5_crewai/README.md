# Phase 5: CrewAI

学习 CrewAI 框架，掌握团队式智能体架构和生产级 AI Agent 应用。

## 学习目标

完成本阶段后，你将能够：

- ✅ 理解 CrewAI 的核心概念（Agent、Task、Crew）
- ✅ 创建角色化的 Agent
- ✅ 定义任务并关联 Agent
- ✅ 使用 Process 管理任务执行流程
- ✅ 集成各种 Tools（工具）
- ✅ 实现生产级 AI Agent 应用
- ✅ 优化 Crew 性能和可靠性

## 前置条件

1. ✅ 已完成 Phase 4（AutoGen）
2. 已在项目根目录配置 `.env` 文件
3. 已安装阶段依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 目录结构

```
phase5_crewai/
├── example/               # AI 生成的示例代码
│   ├── 01_basics.py                   # 基础概念
│   ├── 02_agents.py                   # 创建 Agent
│   ├── 03_tasks.py                    # 定义 Task
│   ├── 04_crew.py                     # 组装 Crew
│   ├── 05_tools.py                    # 集成工具
│   ├── 06_sequential_process.py       # 顺序流程
│   ├── 07_hierarchical_process.py     # 层级流程
│   ├── 08_production_app.py           # 生产级应用
│   └── 09_best_practices.py           # 最佳实践
├── practice/              # 手动练习代码
├── notes/                 # 学习笔记
│   ├── 01_overview.md
│   ├── 02_agents_and_tasks.md
│   ├── 03_processes.md
│   ├── 04_tools_integration.md
│   ├── 05_deployment.md
│   └── 06_best_practices.md
├── tests/                 # 测试文件
├── config/                # 配置文件
└── requirements.txt       # 本阶段依赖
```

## CrewAI 核心概念

### 1. Agent（智能体）

具有特定角色和能力的智能体。

```python
from crewai import Agent

agent = Agent(
    role="高级研究员",
    goal="研究和分析最新技术趋势",
    backstory="你是一名经验丰富的研究员..."
)
```

### 2. Task（任务）

需要完成的具体工作，分配给特定的 Agent。

```python
from crewai import Task

task = Task(
    description="研究 AI Agent 的最新发展",
    expected_output="一份详细的研究报告",
    agent=researcher_agent
)
```

### 3. Crew（团队）

由多个 Agent 和 Task 组成的团队。

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential
)
```

### 4. Tools（工具）

Agent 可以使用的工具函数。

```python
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()
```

### 5. Process（流程）

定义任务执行的顺序和方式。

- **Sequential**: 顺序执行
- **Hierarchical**: 层级执行（有 Manager）

## 学习路径

### 第 1 步：基础概念

**示例代码：** `example/01_basics.py`

**学习重点：**
- Agent、Task、Crew 的关系
- 基本使用流程
- 输入输出处理

### 第 2 步：创建 Agent

**示例代码：** `example/02_agents.py`

**学习重点：**
- 角色定义（Role、Goal、Backstory）
- LLM 配置
- 工具分配

### 第 3 步：定义 Task

**示例代码：** `example/03_tasks.py`

**学习重点：**
- Task 属性（description、expected_output）
- 上下文传递
- 依赖关系

### 第 4 步：组装 Crew

**示例代码：** `example/04_crew.py`

**学习重点：**
- Crew 配置
- 流程选择
- 执行和监控

### 第 5 步：集成工具

**示例代码：** `example/05_tools.py`

**学习重点：**
- 内置工具使用
- 自定义工具开发
- 工具权限管理

### 第 6 步：流程管理

**示例代码：** `example/06_sequential_process.py`、`example/07_hierarchical_process.py`

**学习重点：**
- Sequential 流程
- Hierarchical 流程
- 条件分支

### 第 7 步：生产级应用

**示例代码：** `example/08_production_app.py`

**学习重点：**
- 错误处理
- 日志记录
- 性能优化
- API 部署

## 运行示例

```bash
# 进入阶段目录
cd phase5_crewai

# 运行特定示例
python example/01_basics.py

# 运行所有测试
pytest tests/
```

## CrewAI vs AutoGen vs LangChain

| 特性 | CrewAI | AutoGen | LangChain |
|------|--------|---------|-----------|
| 专注点 | 团队协作 | 多 Agent 对话 | LLM 应用框架 |
| 复杂度 | 中等 | 高 | 低-高 |
| 工具集成 | 丰富 | 基础 | 丰富 |
| 流程控制 | Sequential/Hierarchical | 灵活对话 | Chain |
| 学习曲线 | 中等 | 较陡 | 较平缓 |

## Process 对比

| Process | 特点 | 适用场景 |
|---------|------|----------|
| Sequential | 按顺序执行任务 | 线性工作流 |
| Hierarchical | Manager 协调任务 | 复杂多任务 |

## 常见问题

### 1. Agent 不使用工具？

**解决方案：**
- 确保工具正确分配给 Agent
- 检查工具权限设置
- 在 Task 描述中明确提示使用工具

### 2. 任务依赖不生效？

**解决方案：**
- 使用 `context` 参数传递上下文
- 检查任务执行顺序
- 确认 Process 设置正确

### 3. 性能太慢？

**解决方案：**
- 使用更快的 LLM
- 减少任务数量
- 并行执行独立任务
- 缓存中间结果

## 最佳实践

### 1. Agent 角色设计

```python
agent = Agent(
    role="Python 专家",  # 清晰的角色
    goal="编写高质量、可维护的 Python 代码",  # 明确的目标
    backstory="你是一名资深 Python 开发者，有 10 年经验..."  # 丰富的背景
)
```

### 2. Task 描述规范

```python
task = Task(
    description="""
    任务：编写一个快速排序算法
    要求：
    1. 使用 Python 实现
    2. 添加详细注释
    3. 包含测试用例
    4. 时间复杂度: O(n log n)
    """,
    expected_output="完整的 Python 代码文件"
)
```

### 3. 生产级配置

```python
crew = Crew(
    agents=[],
    tasks=[],
    process=Process.sequential,
    verbose=True,
    memory=True,
    max_rpm=100  # 每分钟最大请求数
)
```

## 下一步

恭喜！你已完成所有学习阶段。

**推荐方向：**
1. 构建自己的 AI Agent 项目
2. 深入研究某个特定框架
3. 探索多模态 Agent
4. 学习 Agent 安全和伦理

---

**开始学习吧！** 👥
