from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import Like, Tweet, User


async def get_like_by_tweet_id_and_user_id(
    tweet_id: Tweet.id, user_id: User.id, session: AsyncSession
) -> Like | None:
    """Получение лайка по id твита и id пользователя"""
    query = select(Like).filter(Like.tweet_id == tweet_id, Like.user_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()
