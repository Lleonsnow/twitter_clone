from sqlalchemy import select, update
from typing import List, Dict, Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.db.base_models import Tweet, User, Like


# async def get_user_likes(user_id: User.id, session: AsyncSession) -> Sequence[Like]:
#     query = select(Like).options(selectinload(Like.user)).filter(Like.user_id == user_id)
#     result = await session.execute(query)
#     return result.scalars().all()


async def get_like_by_tweet_id_and_user_id(tweet_id: Tweet.id, user_id: User.id, session: AsyncSession) -> Like | None:
    query = select(Like).filter(Like.tweet_id == tweet_id, Like.user_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()
