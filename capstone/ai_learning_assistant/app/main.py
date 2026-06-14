"""应用入口：初始化 QApplication 并启动主窗口。"""

import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


def main() -> int:
    """创建应用实例并进入事件循环。"""
    app = QApplication(sys.argv)
    app.setApplicationName("AI Learning Assistant")
    app.setOrganizationName("AILearning")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
