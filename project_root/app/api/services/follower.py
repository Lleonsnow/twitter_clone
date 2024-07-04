from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import Follower, User


async def save_user_followers(followers: Follower, user: User, session: AsyncSession) -> None:
    user.followers.extand(followers)
    session.add(followers)
