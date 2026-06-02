from fastapi import APIRouter, HTTPException, Request
from services.nmap_scanner import run_nmap_scan

router = APIRouter()


@router.get("/nmap_scan")
def nmap_scan(host: str, request: Request):
    if not getattr(request.app.state, "nmap_available", True):
        raise HTTPException(
            status_code=503,
            detail="Nmap n'est pas disponible sur le système. Installez Nmap et vérifiez que le binaire est dans le PATH."
        )

    resultats = run_nmap_scan(host)
    if isinstance(resultats, dict) and resultats.get("error"):
        raise HTTPException(status_code=503, detail=resultats["error"])
    return resultats