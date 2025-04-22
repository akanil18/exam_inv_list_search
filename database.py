import os
import sqlite3

def get_connection():
    # Check if we are in a Render environment (where the database should be in persistent storage)
    if 'RENDER' in os.environ:
        # Use the persistent disk path provided by Render (e.g., `/var/lib/render/db/`)
        db_path = '/var/lib/render/db/invigilation.db'
    else:
        # Local environment (use current working directory)
        db_path = 'invigilation.db'
    
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invigilation_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher TEXT,
            room TEXT,
            date TEXT,
            duration TEXT
        );
    """)
    conn.commit()
    conn.close()

def insert_records(records):
    conn = get_connection()
    cursor = conn.cursor()
    for r in records:
        cursor.execute("""
            INSERT INTO invigilation_records (teacher, room, date, duration)
            VALUES (?, ?, ?, ?);
        """, (r['teacher'], r['room'], r['date'], r['duration']))
    conn.commit()
    conn.close()
