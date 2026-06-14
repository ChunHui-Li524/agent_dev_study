# Phase 6: PySide6 桌面 UI

用 PySide6 构建 **AI 专家** 桌面客户端：聊天界面、后台线程流式输出、LLM/RAG 集成与设置持久化。

## 学习目标

完成本阶段后，你将能够：

- 用 PySide6 搭建主窗口与信号槽交互
- 在 `QThread` 中执行 LLM 调用，避免阻塞 UI
- 将 OpenAI 兼容 API 接入桌面聊天
- 在侧栏展示 RAG 引用来源
- 用 `QSettings` 保存模型与温度等配置

## 前置条件

1. 已完成 Phase 1（API 基础）或具备 OpenAI 客户端使用经验
2. 已在项目根目录或本阶段 `config/` 配置 `.env`（见 `config/.env.example`）
3. 安装依赖：

```bash
cd phase6_ui
pip install -r requirements.txt
```

## 目录结构

```
phase6_ui/
├── example/          # 可运行示例
├── practice/         # 手打练习占位
├── notes/            # 架构笔记
├── config/           # 环境变量示例
└── requirements.txt
```

## 运行示例

```bash
cd phase6_ui
python example/01_pyside6_basics.py
python example/04_integrate_llm.py   # 需配置 API Key
```

## 下一步

完成 UI 原型后，可将 Phase 1–5 的 Agent/RAG 逻辑封装为服务层，再与本阶段界面组合成完整 **AI 学习助手** 桌面应用。

---

**开始搭建桌面端吧！** 🖥️
