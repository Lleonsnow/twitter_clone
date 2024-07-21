from api.core.pydantic_models import BasicResponseSchema
from api.core.validators import chain_validate_from_user
from api.db.base_models import User
from api.db.db import get_db
from api.exceptions.models import ModelException
from api.services.like import set_tweet_like, set_tweet_unlike
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/tweets/{uid}/likes", response_model=BasicResponseSchema)
async def post_tweet_like(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema | ModelException:
    """Лайкнуть пост."""
    result = await set_tweet_like(uid, user, session)
    return (
        JSONResponse(
            content=result.dict(), status_code=int(result.error_message)
        )
        if result
        else BasicResponseSchema(result=True)
    )


@router.delete("/tweets/{uid}/likes", response_model=BasicResponseSchema)
async def delete_tweet_like(
    uid: int,
    user: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> BasicResponseSchema | ModelException:
    """Удалить лайк с поста."""
    result = await set_tweet_unlike(uid, user, session)
    return (
        JSONResponse(
            content=result.dict(), status_code=int(result.error_message)
        )
        if result
        else BasicResponseSchema(result=True)
    )
