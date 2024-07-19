from http import HTTPStatus

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.pydantic_models import ErrorResponse
from app.api.db.base_models import Like as BaseLike, Tweet as BaseTweet, User as BaseUser
from app.api.exceptions.error_handler import error_handler
from app.api.exceptions.models import TweetNotFound
from app.api.services.tweet import get_tweet_by_id


async def set_tweet_like(
    tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession
) -> ErrorResponse | None:
    """Добавление лайка к твиту"""
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
    tweet_id: BaseTweet.id, user_id: BaseUser.id, session: AsyncSession
) -> None:
    """Получение лайка по id твита и id пользователя"""
    query = delete(BaseLike).filter(
        BaseLike.tweet_id == tweet_id, BaseLike.user_id == user_id
    )
    await session.execute(query)
