from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.api.core.settings import Settings

settings = Settings()
DATABASE_URL = settings.base_url.get_secret_value()

async_engine = create_async_engine(
    DATABASE_URL, echo=True, future=True, pool_pre_ping=True
)
async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


class SessionManager:
    """Класс для работы с сессиями SQLAlchemy"""

    def __init__(self, session_factory: async_sessionmaker) -> None:
        self._session_factory = session_factory

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Менеджер сессий SQLAlchemy"""
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


session_manager = SessionManager(async_session)


async def get_db(request: Request) -> AsyncSession:
    """Контекстный менеджер для работы с сессиями SQLAlchemy"""
    return request.state.db
