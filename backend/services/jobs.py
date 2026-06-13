from services.nmap_scanner import run_nmap_scan

JOBS = {}

def run_job(job_id, host):
    JOBS[job_id] = {"status": "running"}
    try:
        JOBS[job_id] = {"status": "done", "result": run_nmap_scan(host)}
    except Exception as e:
        JOBS[job_id] = {"status": "error", "detail": str(e)}