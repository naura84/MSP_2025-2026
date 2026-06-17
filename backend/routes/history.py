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
    cursor.execute("SELECT id, host, type, ports, risque, score, severity, date_scan FROM scans")

    data = cursor.fetchall()

    conn.close()
    
    results = []

    for s in data:
        results.append({
            "id": s[0],
            "host": s[1],
            "type": s[2],
            "ports": s[3],
            "risque": s[4],
            "score": s[5],
            "severity": s[6],
            "date_scan": s[7],
        })

    return {"history" : results}