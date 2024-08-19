import asyncio
import os
from http import HTTPStatus
from typing import BinaryIO, List, Sequence

import aiofiles
from api.core.pydantic_models import ErrorResponse
from api.db.base_models import Media as BaseMedia
from api.exceptions.error_handler import error_handler
from api.exceptions.models import PathNotFoundError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def save_media(
    file: BinaryIO,
    file_name: str,
    session: AsyncSession,
    path: str = "/api/media",
) -> int:
    """Сохраняет медиа-файл локально и возвращает его id."""
    if file_name.endswith("gif"):
        current_path = "/".join((path, "gifs", file_name))
    else:
        current_path = "/".join((path, "photos", file_name))
    async with aiofiles.open(current_path, "wb+") as f:
        await f.write(file.read())

    return await save_media_to_base(current_path, session)


async def save_media_to_base(path: str, session: AsyncSession) -> int:
    """Создает объект медиа-файла в базе данных и возвращает его id."""
    media = BaseMedia(tweet_data=path)
    session.add(media)
    await session.commit()
    await session.refresh(media)
    return media.id


async def get_medias_from_base(
    media_ids: List[int], session: AsyncSession
) -> Sequence[BaseMedia]:
    """Возвращает медиа из базы данных. По id."""
    query = select(BaseMedia).filter(BaseMedia.id.in_(media_ids))
    result = await session.execute(query)
    return result.scalars().all()


async def get_media_from_base(
    media_path: str, session: AsyncSession
) -> ErrorResponse | None:
    """Возвращает медиа из базы данных. По маршруту."""
    query = select(BaseMedia).filter(
        BaseMedia.tweet_data.like(f"%{media_path}%")
    )
    result_query = await session.execute(query)
    result = result_query.scalar()
    if not result:
        return await error_handler(
            PathNotFoundError(
                message="File not found", status=HTTPStatus.NOT_FOUND
            )
        )
    return result


async def delete_local_medias(path_list: Sequence[BaseMedia]) -> None:
    """Удаляет локальные медиа-файлы."""
    loop = asyncio.get_event_loop()

    for media in path_list:
        await loop.run_in_executor(
            None, os.remove, media.tweet_data
        )
