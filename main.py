from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
import datetime

app = FastAPI(title="Universal Identity & Data Gateway")

# --- CONFIGURATION ---
# JWT ko sign karne ke liye secret key. (Production mein yeh environment variables se aati hai)
SECRET_KEY = "my_super_secret_key" 
ALGORITHM = "HS256"

# --- MOCK DATABASE ---
# Assignment ke hisaab se hum ek hardcoded dictionary use kar rahe hain database ki jagah.
MOCK_USERS = {
    "admin": {
        "password": "password123",
        "sub": "user_550e8400-e29b-41d4-a716-446655440000",
        "scopes": ["app_alpha", "service_beta"]
    },
    "sensor_bot": {
        "password": "sensor_password",
        "sub": "device_111e8400-a29b-41d4-a716-112233445566",
        "scopes": ["app_alpha"] # Isko sirf app_alpha ka access hai
    }
}

# --- DTOs (Pydantic Models) ---
# Yeh humara request body format define karta hai
class LoginRequest(BaseModel):
    username: str
    password: str

# --- PHASE 1: IDENTITY ENDPOINT ---
@app.post("/auth/token")
def login_for_access_token(request: LoginRequest):
    # 1. User ko mock database mein dhundho
    user = MOCK_USERS.get(request.username)
    
    # 2. Credentials validate karo (Agar galat hai toh 401 Unauthorized throw karo)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # 3. JWT Payload banate hain (Zero-Trust constraint follow karte hue)
    # Token 1 ghante mein expire ho jayega
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    
    jwt_payload = {
        "sub": user["sub"],           # Unique ID (UUID)
        "scopes": user["scopes"],     # Allowed namespaces
        "exp": expiration_time        # Token expiry time
    }
    
    # 4. JWT Token Generate/Sign karna
    token = jwt.encode(jwt_payload, SECRET_KEY, algorithm=ALGORITHM)
    
    # Response JSON format mein return karna
    return {"access_token": token, "token_type": "bearer"}