"""
==========================================
示例 6: 设置面板与 QSettings
==========================================
学习目标：
1. QDialog 设置表单
2. QDoubleSpinBox 配置 temperature
3. QSettings 持久化模型名与温度
"""

import sys

from PySide6.QtCore import QSettings, Signal
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

SETTINGS_ORG = "AiAgentLearning"
SETTINGS_APP = "Phase6Desktop"
KEY_model = "llm/model"
KEY_temperature = "llm/temperature"


class SettingsDialog(QDialog):
    """模型与温度设置对话框。"""

    settings_saved = Signal(dict)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("设置")
        self._settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        self._setup_ui()
        self._load_from_settings()

    def _setup_ui(self) -> None:
        self._model_edit = QLineEdit()
        self._model_edit.setPlaceholderText("gpt-4o-mini")

        self._temp_spin = QDoubleSpinBox()
        self._temp_spin.setRange(0.0, 2.0)
        self._temp_spin.setSingleStep(0.1)
        self._temp_spin.setDecimals(1)

        form = QFormLayout()
        form.addRow("模型名称", self._model_edit)
        form.addRow("Temperature", self._temp_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_and_close)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def _load_from_settings(self) -> None:
        model = self._settings.value(KEY_model, "gpt-4o-mini")
        temp = float(self._settings.value(KEY_temperature, 0.7))
        self._model_edit.setText(str(model))
        self._temp_spin.setValue(temp)

    def _save_and_close(self) -> None:
        model = self._model_edit.text().strip() or "gpt-4o-mini"
        temp = self._temp_spin.value()
        self._settings.setValue(KEY_model, model)
        self._settings.setValue(KEY_temperature, temp)
        self._settings.sync()
        self.settings_saved.emit({"model": model, "temperature": temp})
        self.accept()


class SettingsDemoWindow(QMainWindow):
    """主窗口：打开设置并显示当前配置。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("设置面板示例")
        self.resize(480, 220)
        self._settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        self._setup_ui()
        self._refresh_label()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        self._info = QLabel()
        self._info.setWordWrap(True)

        open_btn = QPushButton("打开设置…")
        open_btn.clicked.connect(self._open_settings)

        layout = QVBoxLayout(central)
        layout.addWidget(self._info)
        layout.addWidget(open_btn)

    def _open_settings(self) -> None:
        dialog = SettingsDialog(self)
        dialog.settings_saved.connect(self._on_settings_saved)
        dialog.exec()

    def _on_settings_saved(self, _data: dict) -> None:
        self._refresh_label()

    def _refresh_label(self) -> None:
        model = self._settings.value(KEY_model, "gpt-4o-mini")
        temp = self._settings.value(KEY_temperature, 0.7)
        self._info.setText(
            f"当前配置\n模型: {model}\nTemperature: {temp}\n\n"
            "（保存在系统 QSettings，Windows 注册表/配置文件）"
        )


def main() -> None:
    app = QApplication(sys.argv)
    window = SettingsDemoWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
