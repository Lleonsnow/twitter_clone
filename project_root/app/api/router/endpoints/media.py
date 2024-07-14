from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.pydantic_models import MediaResponseSchema
from app.api.core.validators import chain_validate_from_user
from app.api.db.base_models import User
from app.api.db.db import get_db
from app.api.services.media import save_media

router = APIRouter()


@router.post("/medias", response_model=MediaResponseSchema)
async def upload_media(
    file: UploadFile,
    _: User = Depends(chain_validate_from_user),
    session: AsyncSession = Depends(get_db),
) -> MediaResponseSchema:
    """Загрузка медиафайла"""
    media_id = await save_media(file.file, file.filename, session)
    return MediaResponseSchema(result=True, media_id=media_id)


@router.get("/{path:path}", response_class=FileResponse)
async def get_media(
    path: str,
) -> FileResponse:
    """Возвращает медиафайл"""
    return FileResponse(path)
