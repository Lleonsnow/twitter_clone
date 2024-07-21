from typing import NoReturn

from api.db.base_models import User
from api.db.db import get_db
from api.services.api_key import check_api_key
from api.services.user import get_user_by_api_key
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def chain_validate_from_user(
    api_key: str = Header(None), session: AsyncSession = Depends(get_db)
) -> User:
    """Цепочка валидаторов."""
    await verify_api_key(api_key, session)
    return await get_user_by_api_key(api_key, session)


async def verify_api_key(
    api_key: str, session: AsyncSession
) -> None | NoReturn:
    """Верификация API ключа."""
    key = await check_api_key(api_key, session)
    if not key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
