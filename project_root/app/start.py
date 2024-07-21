from contextlib import asynccontextmanager
from typing import Callable

from api.core.settings import Settings
from api.db.base_models import Base
from api.db.db import SessionManager, async_engine
from api.db.db import session_manager as manager
from api.router.router import api_router
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from init_db.data_aggregate import check_aggregate_db, init_test_data
from starlette.middleware.base import BaseHTTPMiddleware


@asynccontextmanager
async def lifespan(*_: FastAPI):
    """Эта функция будет вызвана при запуске приложения и она будет
    использоваться для инициализации базы данных."""

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

        db_created = await check_aggregate_db(manager)
        if not db_created:
            await init_test_data(manager)

    yield
    await async_engine.dispose()


class DBSessionMiddleware(BaseHTTPMiddleware):
    """Класс для создания сессии в контексте запроса."""

    def __init__(self, app: FastAPI, session_manager: SessionManager):
        super().__init__(app)
        self.session_manager = session_manager

    async def dispatch(self, request: Request, call_next: Callable):
        """Эта функция будет вызвана при каждом запросе и она будет
        использоваться для создания сессии."""

        async with self.session_manager.get_session() as session:
            request.state.db = session
            response = await call_next(request)
        return response


settings = Settings()
project_name = settings.project_name
project_version = settings.project_version
app = FastAPI(
    title=project_name, version=project_version, lifespan=lifespan
)
app.include_router(api_router, prefix="/api")
app.mount(
    "/", StaticFiles(directory="api/static", html=True), name="static"
)
app.add_middleware(DBSessionMiddleware, session_manager=manager)
