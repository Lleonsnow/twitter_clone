from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import Follower
from app.api.services.user import get_users


async def save_user_followers(session: AsyncSession) -> None:
    """Создает взаимоотношения между пользователями."""
    users = await get_users(session)
    for user in users:
        following = (user.id + 1) % len(users)
        follower = Follower(follower=user, following=users[following])
        session.add(follower)
