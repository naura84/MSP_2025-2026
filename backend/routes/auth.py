from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth.auth_handler import create_access_token

from core.logger import get_logger
logger = get_logger("auth")

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    logger.info(f"Attempting login for user: {data.username}")
    if data.username != "admin" or data.password != "admin123":
        logger.warning("Login failed: Invalid credentials")
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_access_token(data.username)
    logger.info("Login successful")
    return {"access_token": token}

