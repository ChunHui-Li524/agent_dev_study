"""
==========================================
示例 4: 接入 LLM（非流式）
==========================================
学习目标：
1. load_dotenv 加载 API 配置
2. QThread 调用 OpenAI 兼容接口
3. 在聊天 UI 展示回复
"""

import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# 优先加载阶段 config/.env，再加载项目根 .env
_PHASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(_PHASE_DIR / "config" / ".env")
load_dotenv(_PHASE_DIR.parent / ".env")

SYSTEM_PROMPT = "你是 AI 学习助手，用简洁中文回答。"


def build_client() -> OpenAI:
    """根据环境变量创建 OpenAI 客户端。"""
    kwargs = {"api_key": os.getenv("OPENAI_API_KEY")}
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


class LlmWorker(QThread):
    """后台调用 chat.completions（非流式）。"""

    reply_ready = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, client: OpenAI, user_text: str, parent=None) -> None:
        super().__init__(parent)
        self._client = client
        self._user_text = user_text

    def run(self) -> None:
        try:
            response = self._client.chat.completions.create(
                model=os.getenv("OPENAI_CHAT_model", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": self._user_text},
                ],
                temperature=0.7,
            )
            content = response.choices[0].message.content or ""
            self.reply_ready.emit(content.strip())
        except (RateLimitError, APITimeoutError, APIConnectionError) as exc:
            self.error_occurred.emit(f"API 错误: {exc}")
        except KeyError as exc:
            self.error_occurred.emit(f"响应格式异常: {exc}")


class LlmChatWindow(QMainWindow):
    """带 LLM 后端的聊天窗口。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("接入 LLM 示例")
        self.resize(560, 480)
        self._client = build_client()
        self._worker: LlmWorker | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        self._display = QTextEdit()
        self._display.setReadOnly(True)
        self._display.append("向 AI 提问吧（需配置 OPENAI_API_KEY）。")

        self._input = QLineEdit()
        self._input.setPlaceholderText("例如：什么是 RAG？")
        self._input.returnPressed.connect(self._send)

        self._send_btn = QPushButton("发送")
        self._send_btn.clicked.connect(self._send)

        row = QHBoxLayout()
        row.addWidget(self._input, stretch=1)
        row.addWidget(self._send_btn)

        layout = QVBoxLayout(central)
        layout.addWidget(self._display, stretch=1)
        layout.addLayout(row)

    def _send(self) -> None:
        text = self._input.text().strip()
        if not text or self._worker is not None:
            return
        if not os.getenv("OPENAI_API_KEY"):
            self._append("系统", "请配置 OPENAI_API_KEY")
            return

        self._append("用户", text)
        self._input.clear()
        self._set_busy(True)

        self._worker = LlmWorker(self._client, text, self)
        self._worker.reply_ready.connect(self._on_reply)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.finished.connect(self._cleanup_worker)
        self._worker.start()

    def _append(self, role: str, text: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self._display.append(f"[{ts}] {role}: {text}")

    def _on_reply(self, text: str) -> None:
        self._append("助手", text)

    def _on_error(self, message: str) -> None:
        self._append("系统", message)

    def _cleanup_worker(self) -> None:
        self._worker = None
        self._set_busy(False)

    def _set_busy(self, busy: bool) -> None:
        self._send_btn.setEnabled(not busy)
        self._input.setEnabled(not busy)


def main() -> None:
    app = QApplication(sys.argv)
    window = LlmChatWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
