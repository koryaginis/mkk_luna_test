from fastapi import HTTPException
from app.settings import settings

async def verify_api_key(x_api_key: str):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")