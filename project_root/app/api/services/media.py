from typing import BinaryIO, List, Sequence

import aiofiles
from api.db.base_models import Media as BaseMedia
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
) -> BaseMedia | None:
    """Возвращает медиа из базы данных. По маршруту."""
    if media_path.startswith("/"):
        media_path = media_path.split("/")[-1]
    query = select(BaseMedia).filter(
        BaseMedia.tweet_data.like(f"%{media_path}%")
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()
