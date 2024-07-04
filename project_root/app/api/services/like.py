from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import Tweet, User, Like


async def save_user_likes(tweets: List[Tweet], user: User, session: AsyncSession) -> None:
    for tweet in tweets:
        like = Like(user=user, tweet=tweet)
        session.add(like)
