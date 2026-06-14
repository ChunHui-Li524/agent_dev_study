"""主窗口：菜单栏、聊天面板与来源面板布局（占位实现）。"""

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QWidget

from app.core.config import load_config, save_window_geometry
from app.ui.chat_panel import ChatPanel
from app.ui.source_panel import SourcePanel


class MainWindow(QMainWindow):
    """应用主窗口。"""

    def __init__(self) -> None:
        super().__init__()
        self._config = load_config()
        self._build_menu()
        self._build_central()
        self._apply_geometry()
        self._connect_signals()

    def _build_menu(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("文件(&F)")
        exit_action = QAction("退出(&X)", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("帮助(&H)")
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _build_central(self) -> None:
        central = QWidget()
        layout = QHBoxLayout(central)

        self.chat_panel = ChatPanel()
        self.source_panel = SourcePanel()
        self.source_panel.setMinimumWidth(260)

        layout.addWidget(self.chat_panel, stretch=3)
        layout.addWidget(self.source_panel, stretch=1)

        self.setCentralWidget(central)
        self.setWindowTitle("AI Learning Assistant")

    def _apply_geometry(self) -> None:
        self.resize(
            QSize(self._config.window_width, self._config.window_height)
        )

    def _connect_signals(self) -> None:
        self.chat_panel.message_submitted.connect(self._on_user_message)

    def _on_user_message(self, text: str) -> None:
        """处理用户消息（占位）。"""
        # TODO: 调用 ExpertAgent，更新 source_panel
        self.chat_panel.append_message(
            "助手",
            "（占位回复）ExpertAgent 尚未接入，你的问题是：" + text,
        )
        self.source_panel.set_sources(["TODO: RAG 引用片段 1", "TODO: RAG 引用片段 2"])

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "关于",
            "AI Learning Assistant\nPySide6 + DashScope + RAG + LangChain",
        )

    def closeEvent(self, event) -> None:
        save_window_geometry(self.width(), self.height())
        super().closeEvent(event)
