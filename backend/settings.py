import os
import json
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = APP_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",
    "accent_color": "#00E5FF",
    "font_size": 14,
    "voice_speed": 150,
    "voice_volume": 1.0,
    "remember_me": False,
    "last_username": "",
    "sound_enabled": True,
    "notifications_enabled": True,
    "startup_enabled": False,
    "ai_provider": "openrouter",
    "openrouter_model": "google/gemma-4-31b-it:free",
    "openrouter_api_key": ""
}


def load_settings() -> dict:
    """Load settings from settings.json, creating it with defaults if missing."""
    CONFIG_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all default keys are present (migration/safety)
            for k, v in DEFAULT_SETTINGS.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict) -> bool:
    """Save the settings dictionary to settings.json."""
    CONFIG_DIR.mkdir(exist_ok=True)
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception:
        return False
