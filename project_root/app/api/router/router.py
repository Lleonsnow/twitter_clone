from fastapi import APIRouter

from app.api.core.settings import Settings
from app.api.router.endpoints import tweet, user, media

api_router = APIRouter()
settings = Settings()

api_router.include_router(tweet.router, tags=["tweets"])
api_router.include_router(user.router, tags=["users"])
api_router.include_router(media.router, tags=["media"])
