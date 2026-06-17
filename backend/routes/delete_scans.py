from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sqlite3
from auth.auth_handler import verify_token

security = HTTPBearer()

router = APIRouter()

@router.delete("/delete_scans/{scan_id}")
def delete_scan(scan_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not verify_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    conn = sqlite3.connect("audit.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    conn.commit()
    conn.close()
    return {"deleted": scan_id}