import aiofiles
from typing import BinaryIO, List, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import Media as BaseMedia


async def save_media(
    file: BinaryIO,
    file_name: str,
    session: AsyncSession,
    path: str = "media",
) -> int:
    """Сохраняет медиа-файл локально и возвращает его id"""
    if file_name.endswith("gif"):
        path = "/".join((path, "gifs", file_name))
    else:
        path = "/".join((path, "photos", file_name))
    async with aiofiles.open(path, "wb") as f:
        await f.write(file.read())

    return await save_media_to_base(path, session)


async def save_media_to_base(path: str, session: AsyncSession) -> int:
    """Создает объект медиа-файла в базе данных и возвращает его id"""
    media = BaseMedia(tweet_data=path)
    session.add(media)
    await session.commit()
    await session.refresh(media)
    return media.id


async def get_medias_from_base(
    media_ids: List[int], session: AsyncSession
) -> Sequence[BaseMedia]:
    """Возвращает медиа из базы данных"""
    query = select(BaseMedia).filter(BaseMedia.id.in_(media_ids))
    result = await session.execute(query)
    return result.scalars().all()
