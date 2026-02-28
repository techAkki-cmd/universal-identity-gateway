from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import datetime
import os                    
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Phase 1: Identity Module"])
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_if_env_is_missing")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

MOCK_USERS = {
    "admin": {
        "password": "password123",
        "sub": "user_550e8400-e29b-41d4-a716-446655440000",
        "scopes": ["Database", "service"]
    },
    "sensor_bot": {
        "password": "sensor_password",
        "sub": "device_111e8400-a29b-41d4-a716-112233445566",
        "scopes": ["service"]
    }
}

class LoginRequest(BaseModel):
    username: str
    password: str

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/auth/token")
def login_for_access_token(request: LoginRequest):
    user = MOCK_USERS.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    jwt_payload = {
        "sub": user["sub"],
        "scopes": user["scopes"],
        "exp": expiration_time
    }
    token = jwt.encode(jwt_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}