import os
from pathlib import Path
from PyQt6.QtWidgets import QWidget

# Base class for all loadable plugins
class BasePlugin:
    def get_name(self) -> str:
        """Return the name of the plugin."""
        raise NotImplementedError

    def get_icon(self) -> str:
        """Return the emoji icon representing the plugin."""
        return "🔌"

    def get_widget(self) -> QWidget:
        """Return the widget containing the plugin's UI layout."""
        raise NotImplementedError


def get_stylesheet() -> str:
    """Load QSS styles from resources/styles/theme.qss if it exists, or return dynamic default."""
    APP_ROOT = Path(__file__).resolve().parent.parent
    qss_path = APP_ROOT / "ui/resources/styles/theme.qss"
    if qss_path.exists():
        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass

    # Safe fallback stylesheet with dark Fluent-like look
    return """
        QWidget {
            background-color: #0F172A;
            color: #F8FAFC;
            font-family: "Segoe UI", "Inter", sans-serif;
            font-size: 14px;
        }
        QLineEdit {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 8px;
            color: #F8FAFC;
        }
        QLineEdit:focus {
            border: 1px solid #00E5FF;
        }
        QPushButton {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 10px 16px;
            color: #F8FAFC;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #00E5FF;
            color: #0F172A;
            font-weight: bold;
        }
        QTreeWidget {
            background-color: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 8px;
        }
        QHeaderView::section {
            background-color: #1E293B;
            color: #94A3B8;
            padding: 6px;
            border: none;
            font-weight: bold;
        }
    """
