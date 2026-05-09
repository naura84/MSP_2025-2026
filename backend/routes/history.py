from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/history")
def history():
    
    conn = sqlite3.connect("audit.db")

    cursor = conn.cursor()
    cursor.execute("SELECT host, ports, risque, score, date_scan FROM scans")

    data = cursor.fetchall()

    conn.close()
    
    results = []

    for scan in data:
        results.append({
            "host" : scan[0],
            "ports" : scan[1],
            "risque" : scan[2],
            "score" : scan[3],
            "date_scan" : scan[4]
        })

    return {"history" : results}