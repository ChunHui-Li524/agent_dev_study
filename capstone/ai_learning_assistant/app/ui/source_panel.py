"""来源面板：展示 RAG 检索引用（占位实现）。"""

from PySide6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget


class SourcePanel(QWidget):
    """RAG 引用来源列表。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("引用来源")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)

        self.source_list = QListWidget()
        layout.addWidget(self.source_list, stretch=1)

    def set_sources(self, sources: list[str]) -> None:
        """更新引用列表。"""
        self.source_list.clear()
        for item in sources:
            self.source_list.addItem(item)

    def clear_sources(self) -> None:
        """清空引用列表。"""
        self.source_list.clear()
