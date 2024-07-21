from api.core.settings import Settings
from api.router.endpoints import follower, likes, media, tweet, user
from fastapi import APIRouter

api_router = APIRouter()
settings = Settings()

api_router.include_router(tweet.router, tags=["tweets"])
api_router.include_router(user.router, tags=["users"])
api_router.include_router(media.router, tags=["media"])
api_router.include_router(follower.router, tags=["follow"])
api_router.include_router(likes.router, tags=["likes"])
