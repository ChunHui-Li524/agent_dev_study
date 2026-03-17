---
name: ai_agent_learning_structure_v2
overview: 在 d:/PythonProject/ai_agent 工程中创建五阶段学习目录，每阶段含 example（示例代码）、practice（练习）、notes、tests、config 子目录，各阶段完全独立。
todos:
  - id: create-root-config
    content: 创建根目录配置文件（README.md、.env.example、requirements.txt）
    status: completed
  - id: create-phase1
    content: 创建 phase1_api_basics 目录结构和配置文件（含 example、practice、notes、tests、config 子目录）
    status: completed
    dependencies:
      - create-root-config
  - id: create-phase2
    content: 创建 phase2_langchain 目录结构和配置文件（含 example、practice、notes、tests、config 子目录）
    status: completed
    dependencies:
      - create-root-config
  - id: create-phase3
    content: 创建 phase3_llamaindex 目录结构和配置文件（含 example、practice、notes、tests、config 子目录）
    status: completed
    dependencies:
      - create-root-config
  - id: create-phase4
    content: 创建 phase4_autogen 目录结构和配置文件（含 example、practice、notes、tests、config 子目录）
    status: completed
    dependencies:
      - create-root-config
  - id: create-phase5
    content: 创建 phase5_crewai 目录结构和配置文件（含 example、practice、notes、tests、config 子目录）
    status: completed
    dependencies:
      - create-root-config
---

## 产品概述

创建一个 AI Agent 学习工程，提供从 API 基础到高级框架的全路径学习环境，每个学习阶段独立管理，互不干扰。

## 核心功能

- 创建 5 个学习阶段目录：API 基础、LangChain、LlamaIndex、AutoGen、CrewAI
- 每个阶段包含两个代码目录：example（AI 生成的示例代码）、practice（用户手动练习的空目录）
- 每个阶段包含：笔记目录、测试目录、配置文件、README 说明
- 全局配置：项目主 README、环境变量模板、依赖管理
- 支持多 LLM 提供商配置（OpenAI、国内模型等）
- 每个阶段具备独立的运行环境和示例文件

## Tech Stack

- 开发语言：Python 3.9+
- 虚拟环境管理：venv 或 conda
- 配置管理：python-dotenv
- 依赖管理：requirements.txt
- 测试框架：pytest

## Tech Architecture

### 系统架构

采用分层目录结构设计，每个阶段作为独立模块，全局配置统一管理。使用 .env 文件管理 API 密钥和配置，通过 requirements.txt 分阶段管理依赖。

### 关键决策

- 阶段独立：每个阶段拥有独立的目录结构，避免依赖冲突
- 代码分离：example/ 存放 AI 生成示例，practice/ 存放用户练习代码
- 配置分离：全局配置提供通用设置，阶段配置提供特定设置
- 文档完善：每个阶段包含 README 学习笔记和代码注释

### 架构设计

```
ai_agent/
├── .env.example                    # 全局环境变量模板
├── requirements.txt                 # 全局依赖
├── README.md                        # 项目总览
├── phase1_api_basics/               # 阶段1：API 基础
│   ├── example/                     # AI 生成的示例代码
│   ├── practice/                    # 用户手动练习（空）
│   ├── notes/                       # 学习笔记
│   ├── tests/                       # 测试文件
│   ├── config/                      # 配置文件
│   ├── requirements.txt            # 阶段依赖
│   └── README.md                    # 阶段说明
├── phase2_langchain/                # 阶段2：LangChain
│   └── ...
├── phase3_llamaindex/               # 阶段3：LlamaIndex
│   └── ...
├── phase4_autogen/                  # 阶段4：AutoGen
│   └── ...
└── phase5_crewai/                   # 阶段5：CrewAI
    └── ...
```

## Implementation Details

### 目录结构说明

- **根目录**：存放项目级配置文件和总览文档
- **phaseX_xxx/**：每个学习阶段独立目录，命名格式 phase{序号}_{框架名}
- **example/**：存放 AI 生成的示例代码和实现文件，带完整注释和说明
- **practice/**：存放用户手动练习的代码，初始为空，仅含 .gitkeep 占位文件
- **notes/**：存放学习笔记、markdown 文档
- **tests/**：存放单元测试和集成测试
- **config/**：存放配置文件（API 配置、模型参数等）
- **requirements.txt**：列出该阶段所需的所有 Python 依赖包

### 文件创建策略

- 创建所有目录结构
- 每个目录创建 README.md 或 .gitkeep 文件保留目录结构
- 全局 .env.example 包含多 LLM 提供商配置模板
- 每个阶段的 README.md 包含学习目标、安装步骤、使用示例
- example/ 目录包含带注释的示例代码文件
- practice/ 目录仅包含 .gitkeep 文件

### 依赖管理

- 阶段1（API 基础）：openai、anthropic、zhipuai、dashscope、requests、python-dotenv
- 阶段2（LangChain）：langchain、langchain-openai、langchain-community、langchain-anthropic
- 阶段3（LlamaIndex）：llama-index、llama-index-llms-openai、llama-index-embeddings-openai
- 阶段4（AutoGen）：pyautogen
- 阶段5（CrewAI）：crewai、crewai-tools、langchain-openai

此任务为目录结构创建，不涉及 UI 设计。