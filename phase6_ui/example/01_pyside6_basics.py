"""
==========================================
示例 1: PySide6 基础
==========================================
学习目标：
1. QApplication 与事件循环
2. QMainWindow 与中央控件
3. 按钮点击信号与槽
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """最小主窗口：标签 + 按钮。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PySide6 基础")
        self.resize(420, 180)
        self._click_count = 0
        self._setup_ui()

    def _setup_ui(self) -> None:
        """组装中央布局与信号连接。"""
        central = QWidget()
        self.setCentralWidget(central)

        self._label = QLabel("点击按钮开始")
        self._label.setStyleSheet("font-size: 14px; padding: 8px;")

        self._button = QPushButton("点我")
        self._button.clicked.connect(self._on_button_clicked)

        row = QHBoxLayout()
        row.addWidget(self._button)

        layout = QVBoxLayout(central)
        layout.addWidget(self._label)
        layout.addLayout(row)

    def _on_button_clicked(self) -> None:
        """响应按钮点击，更新标签文案。"""
        self._click_count += 1
        self._label.setText(f"已点击 {self._click_count} 次")


def main() -> None:
    """启动应用。"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
