from http import HTTPStatus

from api.core.pydantic_models import ErrorResponse, MediaResponseSchema
from api.core.validators import chain_validate_from_user
from api.db.base_models import User
from api.db.db import get_db
from api.exceptions.error_handler import error_handler
from api.exceptions.models import ModelException, PathNotFoundError
from api.services.media import get_media_from_base, save_media
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/medias", response_model=MediaResponseSchema)
async def upload_media(
    file: UploadFile,
    _: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> MediaResponseSchema:
    """Загрузка медиафайла."""
    media_id = await save_media(file.file, file.filename, session)
    return MediaResponseSchema(result=True, media_id=media_id)


@router.get("/{path:path}", response_model=ErrorResponse)
async def get_media(
    path: str,
    session: AsyncSession = Depends(get_db),
) -> FileResponse | ModelException:
    """Возвращает медиафайл."""
    media_obj = await get_media_from_base(path, session)
    return (
        error_handler(
            PathNotFoundError(
                message="File not found", status=HTTPStatus.NOT_FOUND
            )
        )
        if not path
        else FileResponse(path=media_obj.tweet_data)
    )
