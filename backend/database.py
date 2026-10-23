
import sqlite3, json, os
from datetime import datetime, timezone
DB_PATH = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "karnataka_yatra.db"))

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            starting_location TEXT NOT NULL,
            budget REAL NOT NULL,
            days INTEGER NOT NULL,
            payload TEXT NOT NULL
        )""")

def save_trip(result):
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO trips(created_at, starting_location, budget, days, payload) VALUES(?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), result["starting_location"], result["budget"], result["days"], json.dumps(result, ensure_ascii=False))
        )
        return cur.lastrowid

def list_saved_trips():
    with connect() as conn:
        rows = conn.execute("SELECT id, created_at, starting_location, budget, days FROM trips ORDER BY id DESC LIMIT 20").fetchall()
        return [dict(row) for row in rows]
