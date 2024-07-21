from api.core.pydantic_models import (
    UserResponseSchema,
    UserWithFollowersSchema,
)
from api.core.validators import chain_validate_from_user
from api.db.base_models import User
from api.db.db import get_db
from api.services.user import get_user_with_followers, user_to_dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/users/me", response_model=UserResponseSchema)
async def get_current_user(
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> UserResponseSchema:
    """Получение текущего пользователя со списком подписчиков."""
    user_with_followers = await get_user_with_followers(user.id, session)
    user_dict = await user_to_dict(user_with_followers)
    return UserResponseSchema(
        result=True, user=UserWithFollowersSchema(**user_dict)
    )


@router.get("/users/{user_id}", response_model=UserResponseSchema)
async def get_user_by_id(
    user_id: int,
    _: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> UserResponseSchema:
    """Получение пользователя по id со списком подписчиков."""
    user_with_followers = await get_user_with_followers(user_id, session)
    user_dict = await user_to_dict(user_with_followers)
    return UserResponseSchema(
        result=True, user=UserWithFollowersSchema(**user_dict)
    )
