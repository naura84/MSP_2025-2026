from fastapi import FastAPI
from routes.scan import router as scan_router
from routes.logs import router as logs_router
from routes.report import router as report_router
from routes.history import router as history_router

app = FastAPI()

app.include_router(scan_router)
app.include_router(logs_router)
app.include_router(report_router)
app.include_router(history_router)


@app.get("/")
def home():
    return {"message": "ca marche"}
