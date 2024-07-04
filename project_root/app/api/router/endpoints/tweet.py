from fastapi import APIRouter, Depends

from app.api.core.pydantic_models import TweetResponse
from app.api.core.validators import chain_validate_from_user
from app.api.services import tweet

router = APIRouter()


@router.get("/tweets", response_model=TweetResponse)
async def get_tweets(api_key: str = Depends(chain_validate_from_user)): ...
