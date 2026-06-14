"""
==========================================
示例 3: QThread 流式输出
==========================================
学习目标：
1. 在 QThread 中执行耗时任务
2. 用 Signal(str) 向 UI 推送流式片段
3. 模拟流式响应（无需真实 API）
"""

import sys
import time

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


MOCK_REPLY = (
    "PySide6 中应把网络请求放在 QThread 里，"
    "通过 Signal 把每个 chunk 传回主线程更新界面，"
    "这样窗口就不会卡住。"
)


class StreamWorker(QThread):
    """后台线程：按字符模拟流式输出。"""

    chunk_received = Signal(str)
    finished_ok = Signal()
    error_occurred = Signal(str)

    def __init__(self, prompt: str, parent=None) -> None:
        super().__init__(parent)
        self._prompt = prompt

    def run(self) -> None:
        """模拟逐字推送（与 prompt 无关的演示回复）。"""
        try:
            _ = self._prompt
            for char in MOCK_REPLY:
                if self.isInterruptionRequested():
                    return
                self.chunk_received.emit(char)
                time.sleep(0.03)
            self.finished_ok.emit()
        except OSError as exc:
            self.error_occurred.emit(str(exc))


class StreamChatWindow(QMainWindow):
    """聊天窗 + 流式 Worker。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QThread 流式示例")
        self.resize(560, 440)
        self._worker: StreamWorker | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        self._display = QTextEdit()
        self._display.setReadOnly(True)

        self._input = QLineEdit()
        self._input.setPlaceholderText("输入任意问题…")
        self._input.returnPressed.connect(self._start_stream)

        self._send_btn = QPushButton("流式发送")
        self._send_btn.clicked.connect(self._start_stream)

        row = QHBoxLayout()
        row.addWidget(self._input, stretch=1)
        row.addWidget(self._send_btn)

        layout = QVBoxLayout(central)
        layout.addWidget(self._display, stretch=1)
        layout.addLayout(row)

    def _start_stream(self) -> None:
        """启动流式 Worker；进行中禁用发送。"""
        prompt = self._input.text().strip()
        if not prompt or self._worker is not None:
            return

        self._display.append(f"\n用户: {prompt}\n助手: ")
        self._input.clear()
        self._set_busy(True)

        self._worker = StreamWorker(prompt, self)
        self._worker.chunk_received.connect(self._on_chunk)
        self._worker.finished_ok.connect(self._on_finished)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.finished.connect(self._cleanup_worker)
        self._worker.start()

    def _on_chunk(self, text: str) -> None:
        """主线程追加流式片段。"""
        cursor = self._display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(text)
        self._display.setTextCursor(cursor)

    def _on_finished(self) -> None:
        self._display.append("")

    def _on_error(self, message: str) -> None:
        self._display.append(f"\n[错误] {message}")

    def _cleanup_worker(self) -> None:
        self._worker = None
        self._set_busy(False)

    def _set_busy(self, busy: bool) -> None:
        self._send_btn.setEnabled(not busy)
        self._input.setEnabled(not busy)


def main() -> None:
    app = QApplication(sys.argv)
    window = StreamChatWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
