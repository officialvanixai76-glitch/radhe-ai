import sys
from datetime import datetime
from backend.database import get_connection

# Windows sound libraries
if sys.platform == "win32":
    import winsound
else:
    winsound = None


def play_sound(sound_type: str = "info"):
    """Play a native OS beep or sound depending on the alert severity level."""
    if not winsound:
        print(f"\aSound: {sound_type}")
        return

    try:
        if sound_type == "info":
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        elif sound_type == "warning":
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        elif sound_type == "error":
            winsound.MessageBeep(winsound.MB_ICONHAND)
        elif sound_type == "success":
            # Play a short custom beep sequence for success
            winsound.Beep(1000, 150)
            winsound.Beep(1500, 150)
        else:
            winsound.Beep(800, 200)
    except Exception:
        pass


def add_reminder(title: str, description: str, due_time: str) -> bool:
    """Save a scheduled reminder to the SQLite database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (title, description, due_time) VALUES (?, ?, ?)",
            (title, description, due_time)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_reminders() -> list:
    """Retrieve all pending reminders from the SQLite database."""
    reminders = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, description, due_time, status FROM reminders WHERE status = 'pending' ORDER BY due_time ASC"
        )
        for row in cursor.fetchall():
            reminders.append({
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "due_time": row["due_time"],
                "status": row["status"]
            })
        conn.close()
    except Exception:
        pass
    return reminders


def complete_reminder(reminder_id: int):
    """Mark a reminder as completed in the SQLite database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reminders SET status = 'completed' WHERE id = ?",
            (reminder_id,)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass
