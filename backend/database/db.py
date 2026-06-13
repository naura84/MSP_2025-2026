import sqlite3

conn = sqlite3.connect("audit.db")

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS scans (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               host TEXT,
               ports TEXT,
               risque TEXT,
               score INTEGER,
               type TEXT,
               date_scan TEXT,
               service TEXT,
               detected_version TEXT,
               cve TEXT,
               severity TEXT,
               description TEXT
               )"""
)

conn.commit()

conn.close()