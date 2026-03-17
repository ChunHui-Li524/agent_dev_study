# AI Agent 学习工程

从 API 基础到高级框架的完整学习路径，逐步掌握 AI Agent 开发技术栈。

## 学习路线

| 阶段 | 框架 | 学习目标 | 状态 |
|------|------|----------|------|
| 1 | API 基础 | 掌握直接调用 OpenAI、Anthropic、国内模型 API 的方法 | 📝 待开始 |
| 2 | LangChain | 学习 LangChain 核心概念：Chain、Agent、Prompt Template | 📝 待开始 |
| 3 | LlamaIndex | 掌握数据索引、检索增强生成（RAG）技术 | 📝 待开始 |
| 4 | AutoGen | 学习多智能体协作、对话管理 | 📝 待开始 |
| 5 | CrewAI | 掌握团队式智能体架构、任务编排 | 📝 待开始 |

## 快速开始

### 环境要求

- Python 3.9+
- 推荐使用虚拟环境（venv 或 conda）

### 初始化步骤

1. **克隆或创建项目目录**
   ```bash
   cd d:/PythonProject/ai_agent
   ```

2. **创建并激活虚拟环境**
   ```bash
   # 使用 venv
   python -m venv venv
   venv\Scripts\activate  # Windows
   
   # 或使用 conda
   conda create -n ai_agent python=3.9
   conda activate ai_agent
   ```

3. **配置环境变量**
   ```bash
   # 复制环境变量模板
   copy .env.example .env  # Windows
   # 或
   cp .env.example .env    # Linux/Mac
   
   # 编辑 .env 文件，填入你的 API 密钥
   notepad .env  # Windows
   # 或
   vim .env       # Linux/Mac
   ```

4. **安装依赖**
   ```bash
   # 安装全局依赖
   pip install -r requirements.txt
   
   # 进入特定阶段目录，安装该阶段依赖
   cd phase1_api_basics
   pip install -r requirements.txt
   ```

## 目录结构

```
ai_agent/
├── .env.example              # 全局环境变量模板
├── requirements.txt           # 全局依赖
├── README.md                  # 项目总览（本文件）
│
├── phase1_api_basics/         # 阶段1：API 基础
│   ├── example/               # AI 生成的示例代码
│   ├── practice/              # 手动练习代码（空）
│   ├── notes/                 # 学习笔记
│   ├── tests/                 # 测试文件
│   ├── config/                # 配置文件
│   ├── requirements.txt       # 阶段依赖
│   └── README.md              # 阶段说明
│
├── phase2_langchain/          # 阶段2：LangChain
│   └── ...
│
├── phase3_llamaindex/         # 阶段3：LlamaIndex
│   └── ...
│
├── phase4_autogen/            # 阶段4：AutoGen
│   └── ...
│
└── phase5_crewai/             # 阶段5：CrewAI
    └── ...
```

## 各阶段说明

### Phase 1: API 基础

学习如何直接调用大语言模型 API，包括：
- OpenAI GPT 系列调用
- Anthropic Claude 调用
- 国内模型（智谱、通义千问、文心一言）调用
- 流式输出、异步调用、错误处理

**推荐学习顺序：**
1. 阅读 `phase1_api_basics/README.md`
2. 学习 `example/` 目录下的示例代码
3. 在 `practice/` 目录手动敲一遍代码
4. 运行 `tests/` 目录下的测试验证

### Phase 2: LangChain

学习 LangChain 框架的核心能力：
- Prompt Template 和 Chain
- Memory（记忆机制）
- Agent（智能体）和 Tools
- Document Loader 和 RAG 基础

### Phase 3: LlamaIndex

深入学习数据索引和检索增强：
- Document Indexing
- Vector Stores
- Query Engine
- RAG 高级应用

### Phase 4: AutoGen

学习多智能体协作：
- Conversable Agent
- Group Chat
- Human-in-the-loop
- 多智能体任务分配

### Phase 5: CrewAI

掌握团队式智能体架构：
- Agent、Task、Crew
- 工具集成
- 流程编排
- 生产级应用

## LLM 提供商配置

本项目支持多个 LLM 提供商，在 `.env` 文件中配置对应的 API 密钥：

- **OpenAI**: `OPENAI_API_KEY`（支持代理地址 `OPENAI_BASE_URL`）
- **Anthropic**: `ANTHROPIC_API_KEY`
- **智谱 AI**: `ZHIPUAI_API_KEY`
- **阿里通义千问**: `DASHSCOPE_API_KEY`
- **百度文心一言**: `QIANFAN_ACCESS_KEY`、`QIANFAN_SECRET_KEY`

## 常见问题

### 1. 如何避免 API 费用过高？

- 控制调用频率
- 使用 cheaper 模型（如 GPT-4o-mini 替代 GPT-4）
- 设置合理的 token 限制
- 在本地测试时使用较小的数据集

### 2. 如何处理网络问题？

- OpenAI API 可能需要配置代理：在 `.env` 中设置 `OPENAI_BASE_URL`
- 国内模型（智谱、通义千问）无需代理
- 检查防火墙设置

### 3. 各阶段是否必须按顺序学习？

- **推荐顺序**：1 → 2 → 3 → 4 → 5
- **灵活调整**：如果已有经验，可跳过某些阶段
- **学习方式**：每个阶段独立，可并行学习

## 参考资源

- [OpenAI API 文档](https://platform.openai.com/docs)
- [Anthropic Claude 文档](https://docs.anthropic.com)
- [LangChain 文档](https://python.langchain.com)
- [LlamaIndex 文档](https://docs.llamaindex.ai)
- [AutoGen 文档](https://microsoft.github.io/autogen)
- [CrewAI 文档](https://docs.crewai.com)

## 许可证

MIT License

---

**开始你的 AI Agent 学习之旅吧！** 🚀
