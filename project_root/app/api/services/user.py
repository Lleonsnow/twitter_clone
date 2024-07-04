from typing import Dict, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import ApiKey, User


async def get_user_by_api_key(api_key: str, session: AsyncSession) -> User:
    query = select(User).join(ApiKey).filter(ApiKey.name == api_key)
    user_orm = await session.execute(query)
    return user_orm.scalar()


async def create_user_flush(user: User, session: AsyncSession) -> User:
    session.add(user)
    await session.flush()
    return user
