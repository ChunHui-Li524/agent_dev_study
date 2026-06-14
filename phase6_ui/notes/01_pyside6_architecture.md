# PySide6 架构：UI / Agent / RAG 分层

## 三层职责

| 层 | 职责 | 典型类 |
|----|------|--------|
| **UI** | 窗口、控件、用户输入展示 | `QMainWindow`, `QWidget`, Signal/Slot |
| **Agent** | 对话编排、Tool 调用、会话状态 | 纯 Python 服务类（无 Qt 依赖） |
| **RAG** | 检索、引用列表、上下文注入 | 向量检索客户端或 Mock 数据源 |

UI 层**不直接**调用 LLM API；通过 Signal 把用户消息交给 Worker / Agent 层，结果再通过 Signal 回传更新控件。

## QThread 流式模式

```
用户点击发送 → UI emit → StreamWorker(QThread) → 循环 emit chunk(str)
                → UI slot appendText → 主线程刷新 QTextEdit
```

要点：

1. 耗时 IO（网络、流式读）放在 `QThread` 或 `QObject` + `moveToThread`
2. 跨线程通信用 `Signal(str)`，槽函数只做轻量 UI 更新
3. Worker 内禁止直接操作 QWidget

## 与 Web（FastAPI SSE）对比

- **桌面**：PySide6 + QThread + Signal，本地体验、可离线打包
- **Web**：FastAPI `StreamingResponse` + SSE，浏览器消费（见 `example/optional_fastapi_sse.py`）

同一套 Agent/RAG 逻辑可共用，仅替换「传输层」（Signal vs SSE）。
