from http import HTTPStatus

from api.core.pydantic_models import ErrorResponse
from api.db.base_models import Like as BaseLike
from api.db.base_models import Tweet as BaseTweet
from api.db.base_models import User as BaseUser
from api.exceptions.error_handler import error_handler
from api.exceptions.models import TweetNotFound
from api.services.tweet import get_tweet_by_id
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


async def set_tweet_like(
    tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession
) -> ErrorResponse | None:
    """Добавление лайка к твиту."""
    tweet = await get_tweet_by_id(tweet_id, session)
    if not tweet:
        return await error_handler(
            error=TweetNotFound(
                status=HTTPStatus.NOT_FOUND, message="Tweet not found"
            )
        )

    like = BaseLike(tweet=tweet, user=user, name=user.name)
    tweet.like_count += 1
    session.add(like)
    await session.commit()


async def set_tweet_unlike(
    tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession
) -> ErrorResponse | None:
    """Получение лайка по id твита и id пользователя."""
    tweet = await get_tweet_by_id(tweet_id, session)
    if not tweet:
        return await error_handler(
            error=TweetNotFound(
                status=HTTPStatus.NOT_FOUND, message="Tweet not found"
            )
        )
    query = delete(BaseLike).filter(
        BaseLike.tweet_id == tweet_id, BaseLike.user_id == user.id
    )
    await session.execute(query)
    tweet.like_count -= 1
    await session.commit()
