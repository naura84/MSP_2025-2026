from fastapi import APIRouter
import sqlite3
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from auth.auth_handler import verify_token, security

router = APIRouter()

@router.get("/history")

# Récupère l'historique des scans depuis la base de données
def history(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401, 
            detail="Token invalide ou expiré"
            )
    
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