from fastapi import APIRouter 
import sqlite3

router = APIRouter()

@router.get("/health")
def health():

    try:

        conn = sqlite3.connect("audit.db")

        conn.close()

        db_status = "Connecté"

    except : 
        db_status = "Déconnecté"

    return {
        "status" : "online",
        "database" : db_status
    }