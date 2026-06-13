from fastapi import FastAPI
from routes.scan import router as scan_router
from routes.logs import router as logs_router
from routes.report import router as report_router
from routes.history import router as history_router
from routes.stats import router as stats_router
from routes.auth import router as auth_router
from routes.health import router as health_router
from routes.nmap_scan import router as nmap_scan_router
from services.nmap_scanner import is_nmap_available
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],       
    allow_headers=["*"],     
)


@app.on_event("startup")
def check_nmap_startup():
    available = is_nmap_available()
    app.state.nmap_available = available
    if not available:
        print("[STARTUP] Nmap non trouvé : installe Nmap et ajoute le binaire nmap au PATH.")

app.include_router(scan_router)
app.include_router(logs_router)
app.include_router(report_router)
app.include_router(history_router)
app.include_router(stats_router)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(nmap_scan_router)


@app.get("/")
def home():
    return {"message": "ca marche"}
