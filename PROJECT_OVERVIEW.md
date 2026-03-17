# AI Agent 学习工程 - 项目概览

## 📁 项目结构

```
d:/PythonProject/ai_agent/
├── README.md                          # 项目总览
├── .env.example                       # 全局环境变量模板
├── requirements.txt                    # 全局依赖
│
├── phase1_api_basics/                 # 阶段一：API 基础
│   ├── example/                       # 示例代码
│   │   ├── 01_openai_basic.py         # OpenAI 基础调用
│   │   └── 02_openai_streaming.py     # 流式输出
│   ├── practice/                      # 练习目录（空）
│   ├── notes/                         # 学习笔记
│   │   └── 01_openai_api.md
│   ├── tests/                         # 测试文件
│   ├── config/                        # 配置文件
│   ├── requirements.txt               # 阶段依赖
│   └── README.md                      # 阶段说明
│
├── phase2_langchain/                  # 阶段二：LangChain
│   ├── example/                       # 示例代码
│   │   └── 01_prompt_template.py      # Prompt Template
│   ├── practice/                      # 练习目录（空）
│   ├── notes/                         # 学习笔记
│   │   └── 01_concepts.md
│   ├── tests/                         # 测试文件
│   ├── config/                        # 配置文件
│   ├── requirements.txt               # 阶段依赖
│   └── README.md                      # 阶段说明
│
├── phase3_llamaindex/                 # 阶段三：LlamaIndex
│   ├── example/                       # 示例代码
│   │   └── 01_document_loader.py      # 文档加载
│   ├── practice/                      # 练习目录（空）
│   ├── notes/                         # 学习笔记
│   │   └── 01_architecture.md
│   ├── tests/                         # 测试文件
│   ├── config/                        # 配置文件
│   ├── requirements.txt               # 阶段依赖
│   └── README.md                      # 阶段说明
│
├── phase4_autogen/                     # 阶段四：AutoGen
│   ├── example/                       # 示例代码
│   │   └── 01_basic_conversation.py   # 基础对话
│   ├── practice/                      # 练习目录（空）
│   ├── notes/                         # 学习笔记
│   │   └── 01_core_concepts.md
│   ├── tests/                         # 测试文件
│   ├── config/                        # 配置文件
│   ├── requirements.txt               # 阶段依赖
│   └── README.md                      # 阶段说明
│
└── phase5_crewai/                      # 阶段五：CrewAI
    ├── example/                       # 示例代码
    │   └── 01_basics.py               # 基础概念
    ├── practice/                      # 练习目录（空）
    ├── notes/                         # 学习笔记
    │   └── 01_overview.md
    ├── tests/                         # 测试文件
    ├── config/                        # 配置文件
    ├── requirements.txt               # 阶段依赖
    └── README.md                      # 阶段说明
```

## 🎯 学习路径

| 阶段 | 框架 | 核心内容 | 示例数 | 笔记数 |
|------|------|----------|--------|--------|
| 1 | API 基础 | OpenAI、Anthropic、国内模型调用 | 2 | 1 |
| 2 | LangChain | Prompt、Chain、Memory、Agent | 1 | 1 |
| 3 | LlamaIndex | 文档加载、索引、RAG | 1 | 1 |
| 4 | AutoGen | 多 Agent 协作、Group Chat | 1 | 1 |
| 5 | CrewAI | Agent、Task、Crew | 1 | 1 |

## 📦 已创建的文件清单

### 根目录文件
- ✅ `README.md` - 项目总览和学习路线
- ✅ `.env.example` - 环境变量模板（支持 OpenAI、Anthropic、智谱、通义千问、文心一言）
- ✅ `requirements.txt` - 全局依赖汇总

### Phase 1: API 基础
- ✅ `README.md` - 阶段说明和学习路径
- ✅ `requirements.txt` - 阶段依赖
- ✅ `config/.env.example` - 阶段环境变量
- ✅ `config/model_configs.json` - 模型配置
- ✅ `example/01_openai_basic.py` - OpenAI 基础调用示例
- ✅ `example/02_openai_streaming.py` - 流式输出示例
- ✅ `notes/01_openai_api.md` - OpenAI API 学习笔记

### Phase 2: LangChain
- ✅ `README.md` - 阶段说明和学习路径
- ✅ `requirements.txt` - 阶段依赖
- ✅ `config/.env.example` - 阶段环境变量
- ✅ `example/01_prompt_template.py` - Prompt Template 示例
- ✅ `notes/01_concepts.md` - LangChain 核心概念笔记

### Phase 3: LlamaIndex
- ✅ `README.md` - 阶段说明和学习路径
- ✅ `requirements.txt` - 阶段依赖
- ✅ `config/.env.example` - 阶段环境变量
- ✅ `example/01_document_loader.py` - 文档加载示例
- ✅ `notes/01_architecture.md` - LlamaIndex 架构笔记

### Phase 4: AutoGen
- ✅ `README.md` - 阶段说明和学习路径
- ✅ `requirements.txt` - 阶段依赖
- ✅ `config/.env.example` - 阶段环境变量
- ✅ `example/01_basic_conversation.py` - 基础对话示例
- ✅ `notes/01_core_concepts.md` - AutoGen 核心概念笔记

### Phase 5: CrewAI
- ✅ `README.md` - 阶段说明和学习路径
- ✅ `requirements.txt` - 阶段依赖
- ✅ `config/.env.example` - 阶段环境变量
- ✅ `example/01_basics.py` - 基础概念示例
- ✅ `notes/01_overview.md` - CrewAI 概览笔记

## 🚀 快速开始

### 1. 配置环境变量

```bash
# 复制环境变量模板
cd d:/PythonProject/ai_agent
copy .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
notepad .env
```

### 2. 安装依赖

```bash
# 安装全局依赖
pip install -r requirements.txt

# 进入特定阶段，安装该阶段依赖
cd phase1_api_basics
pip install -r requirements.txt
```

### 3. 运行示例

```bash
# 运行 Phase 1 示例
cd phase1_api_basics
python example/01_openai_basic.py
```

## 📝 学习建议

1. **按顺序学习**：从 Phase 1 到 Phase 5，循序渐进
2. **先看示例**：理解 `example/` 目录下的代码
3. **动手实践**：在 `practice/` 目录手动敲一遍
4. **阅读笔记**：参考 `notes/` 目录下的学习笔记
5. **运行测试**：使用 `pytest` 验证代码

## 🔧 下一步

项目已创建完成，可以开始学习了！

**推荐从 Phase 1 开始：**
1. 阅读 `phase1_api_basics/README.md`
2. 学习 `example/01_openai_basic.py`
3. 在 `practice/` 目录手动敲代码
4. 阅读笔记 `notes/01_openai_api.md`

---

**祝学习顺利！** 🎉
