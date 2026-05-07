from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "ca marche"}

@app.get("/scan")
def scan():
    return {"scan": "analyse réseau terminée"}

@app.get("/logs")
def logs():
    return {"logs": "analyse des logs terminée"}

@app.get("/report")
def report():
    return {"report": "rapport généré"}