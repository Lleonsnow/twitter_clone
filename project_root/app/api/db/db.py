from sqlalchemy import Engine, event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.api.core.settings import Settings

settings = Settings()
DATABASE_URL = settings.db_test.get_secret_value()
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.close()


# DATABASE_URL = settings.base_url.get_secret_value()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, *_):
    """Установка параметра pragma для async sqlite,
    дающая возможность работы с внешними ключами связанных таблиц"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
