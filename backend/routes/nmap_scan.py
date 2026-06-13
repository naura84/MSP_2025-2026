import uuid
from urllib.parse import urlparse

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from services.nmap_scanner import run_nmap_scan

router = APIRouter()

# Jobs en mémoire (OK pour 1 worker en local)
JOBS = {}


class ScanRequest(BaseModel):
    type: str       # "ip" ou "url"
    target: str


def _resolve_host(scan_type: str, target: str) -> str:
    """Pour une URL, extrait le hostname ; pour une IP, renvoie tel quel."""
    target = target.strip()
    if scan_type == "url":
        parsed = urlparse(target if "://" in target else f"http://{target}")
        host = parsed.hostname
        if not host:
            raise ValueError("URL invalide")
        return host
    return target


def _run_job(job_id: str, host: str, scan_type: str):
    """Exécuté en tâche de fond : lance le scan et stocke le résultat."""
    JOBS[job_id] = {"status": "running"}
    try:
        result = run_nmap_scan(host, scan_type=scan_type)
        if result.get("error"):
            JOBS[job_id] = {"status": "error", "detail": result["error"]}
        else:
            JOBS[job_id] = {"status": "done", "result": result}
    except Exception as e:
        JOBS[job_id] = {"status": "error", "detail": str(e)}


@router.post("/nmap_scan")
def start_scan(req: ScanRequest, bg: BackgroundTasks):
    try:
        host = _resolve_host(req.type, req.target)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "running"}
    bg.add_task(_run_job, job_id, host, req.type)
    return {"job_id": job_id, "status": "running"}


@router.get("/nmap_scan/{job_id}")
def scan_status(job_id: str):
    job = JOBS.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job introuvable")
    return job