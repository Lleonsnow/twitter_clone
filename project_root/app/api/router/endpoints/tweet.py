from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.pydantic_models import TweetResponseSchema, TweetResponsePostSchema, TweetCreateRequest
from app.api.core.validators import chain_validate_from_user
from app.api.db.base_models import User
from app.api.db.db import get_db
from app.api.services.tweet import get_user_tweets, tweets_as_schema, create_new_tweet

router = APIRouter()


@router.get("/tweets", response_model=TweetResponseSchema)
async def get_tweets(user: User = Depends(chain_validate_from_user),
                     session: AsyncSession = Depends(get_db)):
    tweets = await get_user_tweets(user.id, session)
    tweets_schema = await tweets_as_schema(tweets)
    return TweetResponseSchema(result=True, tweets=tweets_schema)


@router.post("/tweets", response_model=TweetResponsePostSchema)
async def post_tweets(request: TweetCreateRequest,
                      user: User = Depends(chain_validate_from_user),
                      session: AsyncSession = Depends(get_db)) -> TweetResponsePostSchema:
    tweet = await create_new_tweet(request, user, session)
    return tweet
