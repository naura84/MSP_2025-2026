from jose import jwt
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta

security = HTTPBearer()

SECRET_KEY = "your_secret_key"

ALGORITHM = "HS256"

def create_access_token(username):

    expiration = datetime.utcnow() + timedelta(hours=1)

    payload = {
        "sub": username,
        "exp": expiration
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload
    
    except jwt.ExpiredSignatureError:
        return None
    
    except jwt.JWTError:
        return None