from api.core.pydantic_models import (
    BasicResponseSchema,
    TweetCreateRequest,
    TweetPostResponseSchema,
    TweetsResponseSchema,
)
from api.core.validators import chain_validate_from_user
from api.db.base_models import User
from api.db.db import get_db
from api.exceptions.models import ModelException
from api.services.tweet import (
    create_new_tweet,
    delete_user_tweet,
    get_all_tweets,
    tweets_as_schema,
)
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/tweets", response_model=TweetsResponseSchema)
async def get_tweets(
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> TweetsResponseSchema:
    """Получение списка твитов."""
    tweets = await get_all_tweets(user, session)
    tweets_schema = await tweets_as_schema(tweets)
    return TweetsResponseSchema(result=True, tweets=tweets_schema)


@router.post("/tweets", response_model=TweetPostResponseSchema)
async def post_tweet(
    request: TweetCreateRequest,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> TweetPostResponseSchema:
    """Создание нового твита."""
    tweet = await create_new_tweet(request, user, session)
    return TweetPostResponseSchema(result=True, tweet_id=tweet.id)


@router.delete("/tweets/{uid}", response_model=BasicResponseSchema)
async def delete_tweet(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema | ModelException:
    """Удаление твита."""
    result = await delete_user_tweet(uid, user, session)
    return (
        JSONResponse(
            content=result.dict(), status_code=int(result.error_message)
        )
        if result
        else BasicResponseSchema(result=True)
    )
