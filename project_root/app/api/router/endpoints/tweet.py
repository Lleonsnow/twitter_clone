from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.pydantic_models import (
    BasicResponseSchema,
    TweetCreateRequest,
    TweetPostResponseSchema,
    TweetsResponseSchema,
)
from app.api.core.validators import chain_validate_from_user
from app.api.db.base_models import User
from app.api.db.db import get_db
from app.api.exceptions.models import ModelException
from app.api.services.tweet import (
    create_new_tweet,
    del_tweet_like,
    delete_user_tweet,
    get_all_tweets,
    set_tweet_like,
    tweets_as_schema,
)

router = APIRouter()


@router.get("/tweets", response_model=TweetsResponseSchema)
async def get_tweets(
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> TweetsResponseSchema:
    tweets = await get_all_tweets(user, session)
    tweets_schema = await tweets_as_schema(tweets)
    return TweetsResponseSchema(result=True, tweets=tweets_schema)


@router.post("/tweets", response_model=TweetPostResponseSchema)
async def post_tweet(
    request: TweetCreateRequest,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> TweetPostResponseSchema:
    tweet = await create_new_tweet(request, user, session)
    return TweetPostResponseSchema(result=True, tweet_id=tweet.id)


@router.post("/tweets/{uid}/likes", response_model=BasicResponseSchema)
async def post_tweet_like(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema | ModelException:
    result = await set_tweet_like(uid, user, session)
    return (
        JSONResponse(
            content=result.dict(), status_code=int(result.error_message)
        )
        if result
        else BasicResponseSchema(result=True)
    )


@router.delete("/tweets/{uid}/likes", response_model=BasicResponseSchema)
async def delete_tweet_like(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema:
    await del_tweet_like(uid, user, session)
    return BasicResponseSchema(result=True)


@router.delete("/tweets/{uid}", response_model=BasicResponseSchema)
async def delete_tweet(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema | ModelException:
    result = await delete_user_tweet(uid, user, session)
    return (
        JSONResponse(
            content=result.dict(), status_code=int(result.error_message)
        )
        if result
        else BasicResponseSchema(result=True)
    )
