from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/history")
def history():
    
    conn = sqlite3.connect("audit.db")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans")

    data = cursor.fetchall()

    conn.close()

    return {"history" : data}