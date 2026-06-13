from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth.auth_handler import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    if data.username != "admin" or data.password != "admin123":
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_access_token(data.username)
    return {"access_token": token}

