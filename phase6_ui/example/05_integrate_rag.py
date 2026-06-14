"""
==========================================
示例 5: 接入 RAG（Mock 引用）
==========================================
学习目标：
1. 主窗口布局：聊天 + 来源侧栏
2. QListWidget 展示 RAG 引用
3. 模拟检索结果与回答联动
"""

import sys
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

MOCK_KNOWLEDGE = {
    "rag": [
        {"source": "data/ai_knowledge/rag_basics.md", "snippet": "RAG：检索增强生成，先检索再生成。"},
        {"source": "data/ai_knowledge/agent_basics.md", "snippet": "Agent 可调用工具完成多步任务。"},
    ],
    "agent": [
        {"source": "data/ai_knowledge/agent_basics.md", "snippet": "Agent = LLM + 规划 + 工具。"},
        {"source": "data/ai_knowledge/function_calling.md", "snippet": "Function Calling 让模型输出结构化工具调用。"},
    ],
    "default": [
        {"source": "data/ai_knowledge/glossary.json", "snippet": "未命中具体主题，返回通用词条。"},
    ],
}


def mock_retrieve(query: str) -> list[dict]:
    """根据关键词返回模拟引用。"""
    q = query.lower()
    if "rag" in q or "检索" in q:
        return MOCK_KNOWLEDGE["rag"]
    if "agent" in q:
        return MOCK_KNOWLEDGE["agent"]
    return MOCK_KNOWLEDGE["default"]


def mock_answer(query: str, hits: list[dict]) -> str:
    """用引用片段拼出演示回答。"""
    snippets = " ".join(h["snippet"] for h in hits[:2])
    return f"关于「{query}」：{snippets}（演示数据，非真实 LLM）"


class RagChatWindow(QMainWindow):
    """聊天 + RAG 来源面板。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RAG 引用示例")
        self.resize(780, 500)
        self._setup_ui()

    def _setup_ui(self) -> None:
        splitter = QSplitter(Qt.Orientation.Horizontal)

        chat_panel = self._build_chat_panel()
        source_panel = self._build_source_panel()

        splitter.addWidget(chat_panel)
        splitter.addWidget(source_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        self.setCentralWidget(splitter)

    def _build_chat_panel(self) -> QWidget:
        panel = QWidget()
        self._display = QTextEdit()
        self._display.setReadOnly(True)

        self._input = QLineEdit()
        self._input.setPlaceholderText("试试：什么是 RAG？或 Agent？")
        self._input.returnPressed.connect(self._on_send)

        self._send_btn = QPushButton("发送")
        self._send_btn.clicked.connect(self._on_send)

        row = QHBoxLayout()
        row.addWidget(self._input, stretch=1)
        row.addWidget(self._send_btn)

        layout = QVBoxLayout(panel)
        layout.addWidget(self._display, stretch=1)
        layout.addLayout(row)
        return panel

    def _build_source_panel(self) -> QWidget:
        panel = QWidget()
        title = QLabel("引用来源")
        title.setStyleSheet("font-weight: bold;")

        self._source_list = QListWidget()

        layout = QVBoxLayout(panel)
        layout.addWidget(title)
        layout.addWidget(self._source_list, stretch=1)
        return panel

    def _on_send(self) -> None:
        query = self._input.text().strip()
        if not query:
            return

        hits = mock_retrieve(query)
        answer = mock_answer(query, hits)

        self._append("用户", query)
        self._append("助手", answer)
        self._update_sources(hits)
        self._input.clear()

    def _append(self, role: str, text: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self._display.append(f"[{ts}] {role}: {text}")

    def _update_sources(self, hits: list[dict]) -> None:
        self._source_list.clear()
        for hit in hits:
            label = f"{hit['source']}\n  {hit['snippet']}"
            self._source_list.addItem(QListWidgetItem(label))


def main() -> None:
    app = QApplication(sys.argv)
    window = RagChatWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
