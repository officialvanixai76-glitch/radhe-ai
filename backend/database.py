import sqlite3
import bcrypt
from datetime import datetime
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = APP_ROOT / "database"
DB_PATH = DB_DIR / "radheai.db"


def get_connection():
    """Return a connection to the SQLite database, creating directory if needed."""
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Create database tables and inject default admin account if not present."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            avatar_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    # Create chat_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            level TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    # Create reminders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_time TIMESTAMP NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    """)

    # Seed default user if empty
    cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    if cursor.fetchone() is None:
        # Default password is 'admin'
        hashed = bcrypt.hashpw(b"admin", bcrypt.gensalt()).decode("utf-8")
        cursor.execute(
            "INSERT INTO users (username, password, avatar_path) VALUES (?, ?, ?)",
            ("admin", hashed, "assets/avatar.png")
        )
        conn.commit()

    conn.close()


def save_log(level: str, message: str):
    """Utility to store a log entry directly into the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (level, message) VALUES (?, ?)",
            (level, message)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_recent_logs(limit: int = 5) -> list:
    """Retrieve the latest log messages from the database logs table."""
    logs = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, level, message FROM logs ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        for row in cursor.fetchall():
            logs.append({
                "timestamp": row["timestamp"],
                "level": row["level"],
                "message": row["message"]
            })
        conn.close()
    except Exception:
        pass
    return logs

