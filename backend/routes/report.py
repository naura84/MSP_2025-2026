from fastapi import APIRouter

router = APIRouter()

@router.get("/report")
def report():
    return {"report" : "report terminé"}