from fastapi import APIRouter, HTTPException

from auth.auth_handler import create_access_token

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):

    if username != "admin" or password != "admin123":

        raise HTTPException(
            status_code=401, 
            detail="Identifiants invalides"
            )
    
    token = create_access_token(username)

    return {
        "access_token": token
    }