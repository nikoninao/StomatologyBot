import sqlite3
import os

DB_PATH = "data/bot.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                day TEXT NOT NULL,
                time TEXT NOT NULL,
                reminded INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def add_user(user_id: int, username: str, full_name: str):
    with get_connection() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
        """, (user_id, username, full_name))
        conn.commit()

def add_booking(user_id: int, day: str, time: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO bookings (user_id, day, time) VALUES (?, ?, ?)",
            (user_id, day, time)
        )
        conn.commit()

def get_bookings(user_id: int):
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, day, time FROM bookings WHERE user_id = ?", (user_id,)
        ).fetchall()

def delete_booking(booking_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()