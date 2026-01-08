import sqlite3

DB_NAME = "anime_app.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

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

    conn.commit()
    conn.close()


# ---------- USER FUNCTIONS ----------

def create_user(username, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
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
        "SELECT user_id FROM users WHERE username=? AND password=?",
        (username, password)
    )
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None


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

def remove_favorite(user_id, anime_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM favorites WHERE user_id=? AND anime_id=?",
        (user_id, anime_id)
    )

    conn.commit()
    conn.close()