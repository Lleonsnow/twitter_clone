from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import Like, Tweet, User


async def delete_like_by_tweet_id_and_user_id(
    tweet_id: Tweet.id, user_id: User.id, session: AsyncSession
) -> None:
    """Получение лайка по id твита и id пользователя"""
    query = delete(Like).filter(
        Like.tweet_id == tweet_id, Like.user_id == user_id
    )
    await session.execute(query)
