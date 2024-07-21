from api.core.pydantic_models import BasicResponseSchema
from api.core.validators import chain_validate_from_user
from api.db.base_models import User
from api.db.db import get_db
from api.services.user import remove_user_follow, save_user_follow
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/users/{uid}/follow", response_model=BasicResponseSchema)
async def post_user_follow(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema:
    """Подписка на пользователя."""
    await save_user_follow(uid, user, session)
    return BasicResponseSchema(result=True)


@router.delete("/users/{uid}/follow", response_model=BasicResponseSchema)
async def delete_user_follow(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema:
    """Отписка от пользователя."""
    await remove_user_follow(uid, user, session)
    return BasicResponseSchema(result=True)
