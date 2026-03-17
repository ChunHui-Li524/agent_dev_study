# AutoGen 核心概念笔记

## AutoGen 是什么？

Microsoft AutoGen 是一个**多智能体对话框架**，让多个 AI Agent 能够协作完成复杂任务。

## 核心架构

```
┌─────────────────┐
│  Group Chat     │  ← 管理多 Agent 交互
│    Manager      │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ↓         ↓        ↓        ↓
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Agent1│ │Agent2│ │Agent3│ │User  │
└──────┘ └──────┘ └──────┘ └──────┘
```

## 核心组件

### 1. Conversable Agent（可对话 Agent）

所有 Agent 的基类，具有发送和接收消息的能力。

```python
from autogen import ConversableAgent

agent = ConversableAgent(
    name="my_agent",
    llm_config={"config_list": config_list}
)
```

**关键参数：**
- `name`: Agent 名称（必须唯一）
- `llm_config`: LLM 配置
- `human_input_mode`: 人工输入模式
- `code_execution_config`: 代码执行配置

### 2. Assistant Agent

使用 LLM 生成回复，提供智能分析和建议。

```python
assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="你是一个 Python 专家。",
    llm_config={"config_list": config_list}
)
```

**特点：**
- 自动使用 LLM 生成回复
- 可以分析代码
- 可以回答问题

### 3. User Proxy Agent

代表用户参与对话，可以执行代码。

```python
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",  # 终止时请求确认
    code_execution_config={"work_dir": "./coding"}
)
```

**human_input_mode 选项：**
- `NEVER`: 完全自动，不请求输入
- `ALWAYS`: 每次都请求输入
- `TERMINATE`: 仅在终止条件时请求输入

**特点：**
- 可以执行 Python 代码
- 可以代表用户确认操作
- 不使用 LLM 生成回复（除非配置）

### 4. Group Chat Manager

管理多个 Agent 的群组对话。

```python
from autogen import GroupChat, GroupChatManager

groupchat = GroupChat(
    agents=[agent1, agent2, agent3],
    messages=[],
    max_round=10
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)
```

## 对话流程

### 1. 两两对话流程

```
User Proxy ─────────────→ Assistant
    ↑                       ↓
    └──────────────────────┘
         （循环直到终止）
```

**代码：**
```python
user_proxy.initiate_chat(
    assistant,
    message="问题"
)
```

### 2. Group Chat 流程

```
Group Chat Manager
         ↓
    选择发言者
         ↓
    ┌────┴────┬─────────┐
    ↓         ↓         ↓
 Agent1    Agent2    Agent3
    ↑         ↑         ↑
    └─────────┴─────────┘
         （循环）
```

**代码：**
```python
user_proxy.initiate_chat(
    manager,
    message="任务"
)
```

## 消息类型

### 1. TEXT_MESSAGE

普通文本消息。

### 2. CODE_MESSAGE

包含代码的消息。

### 3. EXECUTION_RESULT_MESSAGE

代码执行结果。

## 终止条件

### 1. max_consecutive_auto_reply

```python
user_proxy = autogen.UserProxyAgent(
    max_consecutive_auto_reply=5  # 最多 5 次自动回复
)
```

### 2. is_termination_msg

```python
def is_termination_msg(message):
    return "TERMINATE" in message.get("content", "")

user_proxy = autogen.UserProxyAgent(
    is_termination_msg=is_termination_msg
)
```

### 3. 人工干预

```python
user_proxy = autogen.UserProxyAgent(
    human_input_mode="TERMINATE"  # 终止时请求确认
)
```

## 常见模式

### 1. Researcher + Writer

```python
researcher = autogen.AssistantAgent(
    name="researcher",
    system_message="你是一个研究员，负责收集信息。"
)

writer = autogen.AssistantAgent(
    name="writer",
    system_message="你是一个作家，负责撰写内容。"
)
```

### 2. Coder + Reviewer

```python
coder = autogen.AssistantAgent(
    name="coder",
    system_message="你是一个程序员，负责编写代码。"
)

reviewer = autogen.AssistantAgent(
    name="reviewer",
    system_message="你是一个代码审查员，负责审查代码。"
)
```

### 3. Multi-Agent Team

```python
agents = [
    autogen.AssistantAgent(name="planner", system_message="..."),
    autogen.AssistantAgent(name="coder", system_message="..."),
    autogen.AssistantAgent(name="tester", system_message="..."),
    autogen.AssistantAgent(name="reviewer", system_message="..."),
]
```

## 最佳实践

### 1. System Prompt 设计

```python
system_message = """
你是一个 {role}。

职责：
1. {responsibility_1}
2. {responsibility_2}

约束：
- 只处理 {topic}
- 输出格式：{format}
"""
```

### 2. 对话流控制

- 使用 `max_consecutive_auto_reply` 限制长度
- 设置明确的终止条件
- 使用 `human_input_mode` 在关键时刻介入

### 3. 代码执行安全

```python
code_execution_config={
    "work_dir": "./sandbox",  # 隔离目录
    "use_docker": True,  # 使用 Docker 隔离
}
```

## 常见问题

### 1. Agent 重复对话？

**解决方案：**
- 检查 `max_consecutive_auto_reply` 设置
- 调整 System Prompt，要求明确终止

### 2. 代码执行失败？

**解决方案：**
- 检查代码权限
- 查看执行日志
- 确保所需库已安装

### 3. Group Chat 发言顺序混乱？

**解决方案：**
- 使用 `speaker_selection_method` 控制
- 设置 `max_round` 限制轮数
- 在 System Prompt 中明确发言规则

## 参考资源

- [AutoGen 官方文档](https://microsoft.github.io/autogen)
- [AutoGen GitHub](https://github.com/microsoft/autogen)
- [AutoGen Notebooks](https://github.com/microsoft/autogen/tree/main/notebook)
