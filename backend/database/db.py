import sqlite3

conn = sqlite3.connect("audit.db")

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS scans (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               status TEXT,
               risque TEXT
               )"""
)

conn.commit()

conn.close()