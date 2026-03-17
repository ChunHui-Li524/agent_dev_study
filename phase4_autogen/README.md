# Phase 4: AutoGen

学习 Microsoft AutoGen 框架，掌握多智能体协作和对话管理。

## 学习目标

完成本阶段后，你将能够：

- ✅ 理解 AutoGen 的核心架构
- ✅ 创建多个 Conversable Agent
- ✅ 实现 Agent 之间的对话协作
- ✅ 使用 Group Chat 管理多 Agent 交互
- ✅ 实现 Human-in-the-loop（人机协作）
- ✅ 创建自定义 Assistant Agent 和 User Proxy Agent
- ✅ 处理复杂的任务分配和协调

## 前置条件

1. ✅ 已完成 Phase 3（LlamaIndex）
2. 已在项目根目录配置 `.env` 文件
3. 已安装阶段依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 目录结构

```
phase4_autogen/
├── example/               # AI 生成的示例代码
│   ├── 01_basic_conversation.py       # 基础对话
│   ├── 02_assistant_userproxy.py     # Assistant 和 User Proxy
│   ├── 03_group_chat.py               # 群组聊天
│   ├── 04_human_in_loop.py            # 人机协作
│   ├── 05_code_execution.py           # 代码执行
│   ├── 06_multi_agent_task.py         # 多 Agent 任务协作
│   └── 07_custom_agent.py             # 自定义 Agent
├── practice/              # 手动练习代码
├── notes/                 # 学习笔记
│   ├── 01_core_concepts.md
│   ├── 02_agent_types.md
│   ├── 03_conversation_patterns.md
│   ├── 04_group_chat.md
│   └── 05_best_practices.md
├── tests/                 # 测试文件
├── config/                # 配置文件
└── requirements.txt       # 本阶段依赖
```

## AutoGen 核心概念

### 1. Conversable Agent（可对话 Agent）

AutoGen 的核心组件，可以发送和接收消息。

```python
from autogen import ConversableAgent

assistant = ConversableAgent(
    name="assistant",
    llm_config={"model": "gpt-4o-mini"}
)
```

### 2. Assistant Agent

使用 LLM 生成回复。

```python
assistant = ConversableAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)
```

### 3. User Proxy Agent

代表用户，可以执行代码并确认操作。

```python
user_proxy = ConversableAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    code_execution_config={"work_dir": "coding"}
)
```

### 4. Group Chat

管理多个 Agent 之间的群组对话。

```python
from autogen import GroupChat, GroupChatManager

groupchat = GroupChat(
    agents=[assistant, critic, writer],
    messages=[]
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)
```

## 学习路径

### 第 1 步：基础对话

**示例代码：** `example/01_basic_conversation.py`

**学习重点：**
- 创建 Assistant Agent 和 User Proxy Agent
- 发起对话
- 处理对话终止条件

### 第 2 步：Assistant 和 User Proxy 协作

**示例代码：** `example/02_assistant_userproxy.py`

**学习重点：**
- User Proxy 执行代码的能力
- Assistant 分析代码的能力
- 协作循环

### 第 3 步：Group Chat

**示例代码：** `example/03_group_chat.py`

**学习重点：**
- 创建多个角色 Agent
- 配置发言顺序
- 管理对话流程

### 第 4 步：Human-in-the-loop

**示例代码：** `example/04_human_in_loop.py`

**学习重点：**
- 在关键时刻请求人工确认
- 人工干预决策
- 提高系统可控性

### 第 5 步：代码执行

**示例代码：** `example/05_code_execution.py`

**学习重点：**
- 在沙箱中执行代码
- 处理执行结果
- 安全考虑

### 第 6 步：多 Agent 任务协作

**示例代码：** `example/06_multi_agent_task.py`

**学习重点：**
- 任务分解
- Agent 角色分配
- 协同完成复杂任务

## 运行示例

```bash
# 进入阶段目录
cd phase4_autogen

# 运行特定示例
python example/01_basic_conversation.py

# 运行所有测试
pytest tests/
```

## Agent 类型对比

| Agent 类型 | 特点 | 使用场景 |
|------------|------|----------|
| ConversableAgent | 最基础的 Agent，可配置 | 所有场景 |
| AssistantAgent | 专注 LLM 生成 | 文本生成、推理 |
| UserProxyAgent | 代表人，可执行代码 | 代码执行、人工确认 |

## 对话模式

### 1. 两两对话

```
User Proxy ←→ Assistant
```

### 2. 多 Agent 协作

```
User Proxy ←→ Researcher ←→ Writer ←→ Critic
```

### 3. Group Chat

```
      Group Chat Manager
         /     |     \
    Agent1  Agent2  Agent3
```

## 常见问题

### 1. 对话不终止？

**解决方案：**
- 检查 `max_consecutive_auto_reply` 设置
- 调整 termination message
- 使用 `human_input_mode="ALWAYS"`

### 2. Agent 互相攻击？

**解决方案：**
- 设置清晰的 System Prompt
- 限制发言频率
- 使用 Group Chat 管理发言顺序

### 3. 代码执行安全？

**解决方案：**
- 在沙箱环境中执行
- 限制可用的库和函数
- 审查生成的代码

## 下一步

完成本阶段后，进入 **Phase 5: CrewAI**，掌握团队式智能体架构。

---

**开始学习吧！** 🤖
