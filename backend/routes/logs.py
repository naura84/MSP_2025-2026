from fastapi import APIRouter

router = APIRouter()

@router.get("/logs")
def logs():
    return {"logs" : "analyse logs terminée"}