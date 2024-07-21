from api.db.base_models import Follower
from api.services.user import get_users
from sqlalchemy.ext.asyncio import AsyncSession


async def save_user_followers(session: AsyncSession) -> None:
    """Создает взаимоотношения между пользователями."""
    users = await get_users(session)
    for user in users:
        following = (user.id + 1) % len(users)
        follower = Follower(follower=user, following=users[following])
        session.add(follower)
