"""
==========================================
示例 2: 聊天组件
==========================================
学习目标：
1. QTextEdit 只读展示对话
2. QLineEdit 输入与发送按钮
3. 简单消息追加与清空输入
"""

import sys
from datetime import datetime

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


class ChatWidget(QWidget):
    """可复用的聊天面板：展示区 + 输入行。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """创建控件并连接发送逻辑。"""
        self._display = QTextEdit()
        self._display.setReadOnly(True)
        self._display.setPlaceholderText("对话将显示在这里…")

        self._input = QLineEdit()
        self._input.setPlaceholderText("输入消息，Enter 或点击发送")
        self._input.returnPressed.connect(self._send_message)

        self._send_btn = QPushButton("发送")
        self._send_btn.clicked.connect(self._send_message)

        input_row = QHBoxLayout()
        input_row.addWidget(self._input, stretch=1)
        input_row.addWidget(self._send_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self._display, stretch=1)
        layout.addLayout(input_row)

    def _send_message(self) -> None:
        """读取输入框内容并追加到展示区。"""
        text = self._input.text().strip()
        if not text:
            return
        self.append_message("用户", text)
        self._input.clear()

    def append_message(self, role: str, text: str) -> None:
        """按角色格式化并追加一条消息。"""
        ts = datetime.now().strftime("%H:%M:%S")
        self._display.append(f"[{ts}] {role}: {text}")
        self._display.ensureCursorVisible()


class MainWindow(QMainWindow):
    """嵌入 ChatWidget 的主窗口。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("聊天组件示例")
        self.resize(520, 420)
        self.setCentralWidget(ChatWidget())


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
