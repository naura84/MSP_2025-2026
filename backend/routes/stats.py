from fastapi import APIRouter
import sqlite3

router = APIRouter()
@router.get("/stats")
def stats():

    conn = sqlite3.connect("audit.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM scans")
    score_moyen = cursor.fetchone()[0]

    cursor.execute(
        """
SELECT COUNT(*)
FROM scans
WHERE risque = 'élevé'"""
    )
    risque_eleve = cursor.fetchone()[0]

    conn.close()

    return {
        "total_scans" : total_scans,
        "score_moyen" : round(score_moyen, 2) if score_moyen else 0,
        "risque_eleve" : risque_eleve
    }