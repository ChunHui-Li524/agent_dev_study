"""从环境变量与 QSettings 加载应用配置。"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from PySide6.QtCore import QSettings

# 项目根目录：capstone/ai_learning_assistant/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = PROJECT_ROOT / "data" / "ai_knowledge"


@dataclass
class AppConfig:
    """运行时配置快照。"""

    dashscope_api_key: str
    dashscope_base_url: str
    llm_model: str
    embedding_model: str
    knowledge_dir: Path
    window_width: int
    window_height: int


def _load_env() -> None:
    """加载 .env（优先项目根，其次仓库根）。"""
    load_dotenv(PROJECT_ROOT / ".env")
    load_dotenv(PROJECT_ROOT.parents[1] / ".env")


def _read_qsettings() -> QSettings:
    return QSettings("AILearning", "AI Learning Assistant")


def load_config() -> AppConfig:
    """合并环境变量与 QSettings，返回 AppConfig。"""
    _load_env()
    settings = _read_qsettings()

    return AppConfig(
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY", ""),
        dashscope_base_url=os.getenv(
            "DASHSCOPE_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
        llm_model=str(settings.value("llm/model", "qwen-plus")),
        embedding_model=str(settings.value("llm/embedding_model", "text-embedding-v3")),
        knowledge_dir=KNOWLEDGE_DIR,
        window_width=int(settings.value("ui/window_width", 1024)),
        window_height=int(settings.value("ui/window_height", 768)),
    )


def save_window_geometry(width: int, height: int) -> None:
    """持久化窗口尺寸。"""
    settings = _read_qsettings()
    settings.setValue("ui/window_width", width)
    settings.setValue("ui/window_height", height)
