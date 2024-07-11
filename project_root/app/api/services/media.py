import base64
from typing import BinaryIO, List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.db.base_models import Media as BaseMedia


async def save_media(file: BinaryIO, session: AsyncSession) -> int:
    """Сохраняет медиа в базу данных и возвращает его id"""
    media = BaseMedia(tweet_data=file.read())
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
