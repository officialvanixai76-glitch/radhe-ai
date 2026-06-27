import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal
from backend.database import get_connection
from backend.settings import load_settings


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_SYSTEM_PROMPT = (
    "You are RadheAI, a concise, helpful desktop and web assistant. "
    "Help with general questions, system diagnostics, file-management guidance, "
    "and productivity tasks. Keep answers practical and friendly."
)


class ChatMessage:
    def __init__(self, sender: str, message: str, timestamp: str = None):
        self.sender = sender
        self.message = message
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ChatWorker(QObject):
    """Worker to support streaming/non-blocking response generation."""
    word_received = pyqtSignal(str)  # Emitted for streaming words
    finished = pyqtSignal(str)       # Emitted when complete response is ready

    def __init__(self, user_message: str):
        super().__init__()
        self.user_message = user_message

    def run(self):
        """Generate response sequentially word-by-word to emulate streaming."""
        reply = generate_reply(self.user_message)
        
        words = reply.split(" ")
        collected = []
        for word in words:
            time.sleep(0.05) # Simulate latency
            self.word_received.emit(word + " ")
            collected.append(word)

        self.finished.emit(" ".join(collected))


def _settings_api_key(settings: dict) -> str:
    return (
        os.environ.get("RADHEAI_OPENROUTER_API_KEY")
        or settings.get("openrouter_api_key", "")
    ).strip()


def _history_for_openrouter(limit: int = 12) -> list:
    messages = [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT}]
    for msg in get_all_messages()[-limit:]:
        role = "user" if msg.sender.lower() in {"you", "user"} else "assistant"
        messages.append({"role": role, "content": msg.message})
    return messages


def generate_reply(user_message: str) -> str:
    """Generate a chat reply through OpenRouter with a local fallback on errors."""
    settings = load_settings()
    model = settings.get("openrouter_model", "google/gemma-4-31b-it:free")
    api_key = _settings_api_key(settings)

    if not api_key:
        return (
            "OpenRouter is selected, but no API key is configured. "
            "Add openrouter_api_key in config/settings.json or set RADHEAI_OPENROUTER_API_KEY."
        )

    messages = _history_for_openrouter()
    if not messages or messages[-1].get("content") != user_message:
        messages.append({"role": "user", "content": user_message})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 900
    }
    request = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "RadheAI"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        return f"OpenRouter request failed ({exc.code}). {error_body[:300]}"
    except Exception as exc:
        return f"OpenRouter connection failed: {exc}"


def get_all_messages() -> list:
    """Retrieve all logged chat history from the SQLite database."""
    messages = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT sender, message, timestamp FROM chat_history ORDER BY id ASC")
        for row in cursor.fetchall():
            messages.append(ChatMessage(row['sender'], row['message'], row['timestamp']))
        conn.close()
    except Exception:
        pass
    return messages


def add_message(sender: str, message: str):
    """Save a chat message to the SQLite database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (sender, message) VALUES (?, ?)",
            (sender, message)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def clear_history():
    """Delete all chat logs from the SQLite database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history")
        conn.commit()
        conn.close()
    except Exception:
        pass
