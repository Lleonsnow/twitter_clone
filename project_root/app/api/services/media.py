import base64
from typing import List, BinaryIO, Sequence

from sqlalchemy import select

from app.api.db.base_models import Media as BaseMedia

from sqlalchemy.ext.asyncio import AsyncSession


async def bytes_to_str(media: bytes) -> str:
    return base64.b64encode(media).decode('utf-8')


async def save_media(file: BinaryIO, session: AsyncSession) -> int:
    media = BaseMedia(tweet_data=file.read())
    session.add(media)
    await session.commit()
    await session.refresh(media)
    return media.id


async def get_medias_from_base(media_ids: List[int], session: AsyncSession) -> Sequence[BaseMedia]:
    query = select(BaseMedia).filter(BaseMedia.id.in_(media_ids))
    result = await session.execute(query)
    return result.scalars().all()
