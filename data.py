from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any

from auth import verify_jwt

router = APIRouter(tags=["Phase 2: Agnostic Data Ingestor"])

class DataEnvelope(BaseModel):
    source_namespace: str
    metric_category: str
    timestamp: str
    payload: Dict[str, Any]

@router.post("/data/ingest")
def ingest_data(data: DataEnvelope, token_payload: dict = Depends(verify_jwt)):
    allowed_scopes = token_payload.get("scopes", [])
    if data.source_namespace not in allowed_scopes:
        raise HTTPException(
            status_code=403, 
            detail=f"Token access for '{data.source_namespace}' is not there for you."
        )
    
    user_uuid = token_payload.get("sub")
    
    database_record = {
        "user_uuid": user_uuid,
        "envelope": data.model_dump()
    }
    
    print("\n" + "="*40)
    print("--- NEW DATA RECORD INGESTED ---")
    print(database_record)
    print("="*40 + "\n")
    
    return {"status": "success", "message": "Data securely ingested and logged."}