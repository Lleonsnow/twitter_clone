from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.pydantic_models import (
    BasicResponseSchema,
    UserResponseSchema,
    UserWithFollowersSchema,
)
from app.api.core.validators import chain_validate_from_user
from app.api.db.base_models import User
from app.api.db.db import get_db
from app.api.services.user import (
    get_user_with_followers,
    remove_user_follow,
    save_user_follow,
    user_to_dict,
)

router = APIRouter()


@router.get("/users/me", response_model=UserResponseSchema)
async def get_current_user(
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> UserResponseSchema:
    """Получение текущего пользователя со списком подписчиков"""
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
    """Получение пользователя по id со списком подписчиков"""
    user_with_followers = await get_user_with_followers(user_id, session)
    user_dict = await user_to_dict(user_with_followers)
    return UserResponseSchema(
        result=True, user=UserWithFollowersSchema(**user_dict)
    )


@router.post("/users/{uid}/follow", response_model=BasicResponseSchema)
async def post_user_follow(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema:
    """Подписка на пользователя"""
    await save_user_follow(uid, user, session)
    return BasicResponseSchema(result=True)


@router.delete("/users/{uid}/follow", response_model=BasicResponseSchema)
async def delete_user_follow(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema:
    """Отписка от пользователя"""
    await remove_user_follow(uid, user, session)
    return BasicResponseSchema(result=True)
