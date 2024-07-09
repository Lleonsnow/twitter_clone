from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.pydantic_models import TweetResponseSchema, TweetResponsePostSchema, TweetCreateRequest, \
    ResponseSchema
from app.api.core.validators import chain_validate_from_user
from app.api.db.base_models import User
from app.api.db.db import get_db
from app.api.exceptions.models import ModelException
from app.api.services.tweet import get_user_tweets, tweets_as_schema, create_new_tweet, set_tweet_like, del_tweet_like, \
    delete_user_tweet

router = APIRouter()


@router.get("/tweets", response_model=TweetResponseSchema)
async def get_tweets(_: User = Depends(chain_validate_from_user),
                     session: AsyncSession = Depends(get_db)):
    tweets = await get_user_tweets(session)
    tweets_schema = await tweets_as_schema(tweets)
    print(tweets_schema)
    return TweetResponseSchema(result=True, tweets=tweets_schema)


@router.post("/tweets", response_model=TweetResponsePostSchema)
async def post_tweet(request: TweetCreateRequest,
                     user: User = Depends(chain_validate_from_user),
                     session: AsyncSession = Depends(get_db)) -> TweetResponsePostSchema:
    tweet = await create_new_tweet(request, user, session)
    return tweet


@router.post("/tweets/{id}/likes", response_model=ResponseSchema)
async def post_tweet_like(id: int, user: User = Depends(chain_validate_from_user),
                          session: AsyncSession = Depends(get_db)):
    await set_tweet_like(id, user, session)
    return ResponseSchema(result=True)


@router.delete("/tweets/{id}/likes", response_model=ResponseSchema)
async def delete_tweet_like(id: int, user: User = Depends(chain_validate_from_user),
                            session: AsyncSession = Depends(get_db)):
    await del_tweet_like(id, user, session)
    return ResponseSchema(result=True)


@router.delete("/tweets/{uid}", response_model=ResponseSchema)
async def delete_tweet(uid: int, user: User = Depends(chain_validate_from_user),
                       session: AsyncSession = Depends(get_db)) -> ResponseSchema | ModelException:
    result = await delete_user_tweet(uid, user, session)
    return result if result else ResponseSchema(result=True)


# @router.delete("/tweets/")