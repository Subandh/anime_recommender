import os
import sqlite3
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load env vars (optional .env)
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "anime_app.db")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table (include security question fields)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        security_question TEXT,
        security_answer TEXT
    )
    """)

    # If table existed without security columns, add them
    cursor.execute("PRAGMA table_info(users)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'security_question' not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN security_question TEXT")
    if 'security_answer' not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN security_answer TEXT")

    # Favorites table 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        anime_id INTEGER,
        anime_name TEXT,
        UNIQUE(user_id, anime_id)
    )
    """)

    # Password reset tokens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS password_resets (
        token TEXT PRIMARY KEY,
        user_id INTEGER,
        expires_at INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ---------- USER FUNCTIONS ----------

def create_user(username, password, security_question=None, security_answer=None):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        hashed = pwd_context.hash(password)
        sec_q = security_question
        sec_a = None
        if security_answer:
            sec_a = pwd_context.hash(security_answer)

        cursor.execute(
            "INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)",
            (username, hashed, sec_q, sec_a)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, password FROM users WHERE username=?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row and pwd_context.verify(password, row[1]):
        return row[0]
    return None


# ---------- PASSWORD RESET FUNCTIONS ----------
import secrets
import time


def create_password_reset_token(username, expiry_seconds=3600):
    """Create a single-use password reset token for the given username.
    Returns the token string, or None if user not found.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    user_id = row[0]
    token = secrets.token_urlsafe(32)
    expires_at = int(time.time()) + int(expiry_seconds)

    cursor.execute(
        "INSERT INTO password_resets (token, user_id, expires_at) VALUES (?, ?, ?)",
        (token, user_id, expires_at)
    )
    conn.commit()
    conn.close()

    return token


def verify_reset_token(token):
    """Verify token and return user_id if valid, else None."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, expires_at FROM password_resets WHERE token=?", (token,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    user_id, expires_at = row
    if int(time.time()) <= int(expires_at):
        return user_id
    return None


def reset_password(token, new_password):
    """Reset password using a valid token. Returns True on success."""
    user_id = verify_reset_token(token)
    if not user_id:
        return False

    hashed = pwd_context.hash(new_password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=? WHERE user_id=?", (hashed, user_id))
    cursor.execute("DELETE FROM password_resets WHERE token=?", (token,))
    conn.commit()
    conn.close()
    return True


# ---------- FAVORITES FUNCTIONS ----------

def add_favorite(user_id, anime_id, anime_name):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO favorites (user_id, anime_id, anime_name) VALUES (?, ?, ?)",
            (user_id, anime_id, anime_name)
        )

        conn.commit()
        conn.close()
    except Exception as e:
        print("Error adding favorite:", e)


def get_favorites(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT anime_id, anime_name FROM favorites WHERE user_id=?",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows  # [(anime_id, anime_name)]


def get_security_question(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT security_question FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] else None


def verify_security_answer(username, answer):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT security_answer FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    if not row or not row[0]:
        return False
    try:
        return pwd_context.verify(answer, row[0])
    except Exception:
        return False


def reset_password_with_security_answer(username, answer, new_password):
    if not verify_security_answer(username, answer):
        return False
    hashed = pwd_context.hash(new_password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed, username))
    conn.commit()
    conn.close()
    return True

def remove_favorite(user_id, anime_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM favorites WHERE user_id=? AND anime_id=?",
        (user_id, anime_id)
    )

    conn.commit()
    conn.close()