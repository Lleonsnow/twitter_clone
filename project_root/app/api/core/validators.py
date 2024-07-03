from app.api.core.settings import Settings
from fastapi import Header, HTTPException

settings = Settings()


async def verify_api_key(api_key: str = Header(None)):
    if api_key != settings.api_key.get_secret_value():
        raise HTTPException(status_code=401, detail="Invalid API Key")