from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import ApiKey, User


async def check_api_key(api_key: str, session: AsyncSession) -> bool:
    query = select(ApiKey).filter(ApiKey.name == api_key)
    api_key_orm = await session.execute(query)
    return bool(api_key_orm.scalar())


async def save_user_api_key(api_key: ApiKey, user: User, session: AsyncSession) -> None:
    api_key.user = user
    session.add(api_key)
