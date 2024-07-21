from api.db.base_models import ApiKey, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def check_api_key(api_key: str, session: AsyncSession) -> bool:
    """Проверка существования API ключа."""
    query = select(ApiKey).filter(ApiKey.name == api_key)
    api_key_orm = await session.execute(query)
    return bool(api_key_orm.scalar())


async def save_user_api_key(
    api_key: ApiKey, user: User, session: AsyncSession
) -> None:
    """Сохранение API ключа у пользователя."""
    api_key.user = user
    session.add(api_key)
