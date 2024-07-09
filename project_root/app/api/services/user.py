from collections.abc import Sequence
from typing import Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.db.base_models import ApiKey, User, Follower


async def get_user_by_api_key(api_key: str, session: AsyncSession) -> User | None:
    query = select(User).join(ApiKey).filter(ApiKey.name == api_key)
    user_orm = await session.execute(query)
    return user_orm.scalar_one_or_none()


async def get_user_by_id(user_id: User.id, session: AsyncSession) -> User | None:
    query = select(User).filter(User.id == user_id)
    user_orm = await session.execute(query)
    return user_orm.scalar()


async def get_users(session: AsyncSession) -> Sequence[User]:
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user_with_followers(user_id: User.id, session: AsyncSession) -> User | None:
    query = (
        select(User)
        .options(
            selectinload(User.followers).selectinload(Follower.follower),
            selectinload(User.following).selectinload(Follower.following)
        )
        .filter(User.id == user_id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_user_flush(user: User, session: AsyncSession) -> User:
    session.add(user)
    await session.flush()
    return user


async def user_to_dict(user: User | Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": user.id,
        "name": user.name,
        "followers": [{"id": follower.follower.id, "name": follower.follower.name} for follower in user.followers],
        "following": [{"id": follow.following.id, "name": follow.following.name} for follow in user.following]
    }


async def save_user_follow(user_id: int, user: User, session: AsyncSession) -> None:
    following = await get_user_by_id(user_id, session)
    follower = Follower(follower=user, following=following)
    session.add(follower)
    await session.commit()


async def remove_user_follow(user_id: int, user: User, session: AsyncSession) -> None:
    following = await get_user_by_id(user_id, session)
    await session.delete(following)
    await session.commit()
