from fastapi import APIRouter
from services.scanner import run_scan

router = APIRouter()

@router.get("/scan")
def scan(host : str):
    resultats = run_scan(host)

    return resultats

