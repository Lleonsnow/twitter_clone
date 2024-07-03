from fastapi import APIRouter
from app.api.core.settings import Settings
from app.api.router.endpoints import followers, user, likes, twits

api_router = APIRouter()
settings = Settings()

api_router.include_router(twits.router, tags=["twits"])
api_router.include_router(likes.router, tags=["likes"])
api_router.include_router(followers.router, tags=["followers"])
api_router.include_router(user.router, tags=["users"])
