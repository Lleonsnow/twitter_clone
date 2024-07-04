from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import Tweet, User
from app.api.db.db import get_session


async def save_user_tweets(tweets: List[Tweet], user: User, session: AsyncSession) -> None:
    user.tweets.extand(tweets)
    session.add(tweets)
