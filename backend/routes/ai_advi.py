from services.ai_advisor import generate_recommendations
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AdviceRequest(BaseModel):
    scan_result: dict

@router.post("/recommendations")
def recommendations(req: AdviceRequest):
    return generate_recommendations(req.scan_result)