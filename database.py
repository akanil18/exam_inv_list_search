# backend/database.py
import sqlite3

def get_connection():
    conn = sqlite3.connect("invigilation.db", check_same_thread=False)
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
