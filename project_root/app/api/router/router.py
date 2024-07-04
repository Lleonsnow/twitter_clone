from fastapi import APIRouter

from app.api.core.settings import Settings
from app.api.router.endpoints import follower, like, tweet, user

api_router = APIRouter()
settings = Settings()

api_router.include_router(tweet.router, tags=["tweets"])
api_router.include_router(like.router, tags=["likes"])
api_router.include_router(follower.router, tags=["followers"])
api_router.include_router(user.router, tags=["users"])
