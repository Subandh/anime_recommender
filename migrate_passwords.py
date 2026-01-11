"""
Migration script to detect plaintext passwords and re-hash them using passlib.
Run from repo root: python migrate_passwords.py
"""
import os
import sqlite3
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "anime_app.db")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def is_hashed(pw: str) -> bool:
    # CryptContext.identify can be used but is not always present for raw strings
    try:
        return pwd_context.identify(pw) is not None
    except Exception:
        return False


def migrate():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, username, password FROM users")
    rows = cursor.fetchall()

    migrated = 0
    for user_id, username, password in rows:
        if password is None:
            continue
        if is_hashed(password):
            continue
        # Treat as plaintext -> hash and update
        hashed = pwd_context.hash(password)
        cursor.execute("UPDATE users SET password=? WHERE user_id=?", (hashed, user_id))
        migrated += 1
        print(f"Migrated user {username} (id={user_id})")

    conn.commit()
    conn.close()
    print(f"Migration complete. {migrated} passwords hashed.")


if __name__ == '__main__':
    migrate()
