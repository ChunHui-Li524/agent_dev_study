# PyInstaller 打包 PySide6 桌面应用（Windows）

> 选修：将 `example/` 中的聊天客户端打成可执行文件。

## 1. 安装依赖

```bash
pip install pyinstaller pyside6 python-dotenv openai
```

## 2. 基本命令

在 `phase6_ui` 目录下，以 `04_integrate_llm.py` 为例：

```bash
pyinstaller --name AiExpertDesktop ^
  --windowed ^
  --collect-all PySide6 ^
  example/04_integrate_llm.py
```

- `--windowed`：不弹出控制台（GUI 应用）
- `--collect-all PySide6`：收集 Qt 插件与平台依赖（Windows 上很重要）

产物在 `dist/AiExpertDesktop/` 或单文件 `dist/AiExpertDesktop.exe`（若加 `--onefile`）。

## 3. 常见问题

### 缺少 Qt 平台插件

症状：启动报错 `Could not load the Qt platform plugin "windows"`。

处理：确保使用 `--collect-all PySide6`，或手动 `--add-data` 复制 `PySide6/plugins/platforms`。

### .env 未被打包

PyInstaller 不会自动包含 `.env`。可选方案：

1. 发布包旁放置 `config/.env` 说明，让用户自行配置
2. 在 spec 文件中 `datas=[('config/.env.example', 'config')]` 仅作模板
3. 运行时从 `%APPDATA%/AiAgentLearning/` 读取配置

### 单文件 vs 目录

| 模式 | 优点 | 缺点 |
|------|------|------|
| `--onefile` | 分发简单 | 启动慢、体积大 |
| 默认目录模式 | 启动快 | 文件多 |

桌面 AI 客户端推荐**目录模式**便于更新资源。

## 4. spec 文件微调（可选）

```bash
pyi-makespec --windowed --collect-all PySide6 example/04_integrate_llm.py
```

编辑生成的 `04_integrate_llm.spec`，加入 `hiddenimports`、`datas` 后：

```bash
pyinstaller 04_integrate_llm.spec
```

## 5. 图标与版本

```bash
pyinstaller ... --icon=assets/app.ico --version-file=version.txt
```

## 6. 与 Web 版对比

- **PyInstaller + PySide6**：本地桌面，适合内网或离线演示
- **FastAPI SSE**（见 `optional_fastapi_sse.py`）：浏览器访问，部署在服务器

两者可共用同一 Agent/RAG Python 模块，仅 UI 层不同。
