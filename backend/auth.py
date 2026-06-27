import bcrypt
from backend.database import get_connection


def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return False

    stored_hash = row[0].encode()

    return bcrypt.checkpw(password.encode(), stored_hash)