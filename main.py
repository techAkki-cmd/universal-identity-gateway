from fastapi import FastAPI

from auth import router as auth_router
from data import router as data_router

app = FastAPI(
    title="Universal Identity & Data Gateway",
    description="A centralized PaaS-based API Gateway that separates identity management from data ingestion for better scalability and flexibility..",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(data_router)

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "Gateway is modular and running smoothly!"}