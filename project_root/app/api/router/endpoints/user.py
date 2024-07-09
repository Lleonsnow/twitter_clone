from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.pydantic_models import (
    UserProfileSchema,
    UserResponseSchema,
)
from app.api.core.validators import chain_validate_from_user
from app.api.db.base_models import User
from app.api.services.user import get_user_with_followers, user_to_dict
from app.api.db.db import get_db

router = APIRouter()


@router.get("/users/me", response_model=UserResponseSchema)
@router.get("/users/{user_id}", response_model=UserResponseSchema)
async def get_current_user(user: User = Depends(chain_validate_from_user), session: AsyncSession = Depends(get_db)):
    user_with_followers = await get_user_with_followers(user.id, session)
    user_dict = await user_to_dict(user_with_followers)

    return UserResponseSchema(result=True, user=UserProfileSchema(**user_dict))



