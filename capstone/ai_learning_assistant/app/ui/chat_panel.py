"""聊天面板：消息展示与用户输入（占位实现）。"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ChatPanel(QWidget):
    """对话区域：上方历史、下方输入框与发送按钮。"""

    message_submitted = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setPlaceholderText("对话历史将显示在这里…")
        layout.addWidget(self.display, stretch=1)

        input_row = QHBoxLayout()
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("输入你的 AI 学习问题…")
        self.input_box.setMaximumHeight(80)
        input_row.addWidget(self.input_box, stretch=1)

        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self._on_send_clicked)
        input_row.addWidget(self.send_button)

        layout.addLayout(input_row)

    def _on_send_clicked(self) -> None:
        text = self.input_box.toPlainText().strip()
        if not text:
            return
        self.input_box.clear()
        self.append_message("用户", text)
        self.message_submitted.emit(text)

    def append_message(self, role: str, content: str) -> None:
        """向展示区追加一条消息。"""
        self.display.append(f"**{role}**: {content}\n")

    def clear_history(self) -> None:
        """清空对话历史。"""
        self.display.clear()
