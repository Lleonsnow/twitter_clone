from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.core.settings import Settings
from app.api.db.base_models import Base
from app.api.db.db import SessionManager, async_engine
from app.api.db.db import session_manager as manager
from app.api.router.router import api_router
from tests.data_aggregate import check_aggregate_db, init_test_data


@asynccontextmanager
async def lifespan(*_: FastAPI):
    """Эта функция будет вызвана при запуске приложения
    и она будет использоваться для инициализации базы данных"""

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

        db_created = await check_aggregate_db(manager)
        if not db_created:
            await init_test_data(manager)

    yield
    await async_engine.dispose()


class DBSessionMiddleware(BaseHTTPMiddleware):
    """Класс для создания сессии в контексте запроса"""

    def __init__(self, app: FastAPI, session_manager: SessionManager):
        super().__init__(app)
        self.session_manager = session_manager

    async def dispatch(self, request: Request, call_next: Callable):
        """Эта функция будет вызвана при каждом запросе
        и она будет использоваться для создания сессии"""
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
    "/", StaticFiles(directory="app/api/static", html=True), name="static"
)
app.add_middleware(DBSessionMiddleware, session_manager=manager)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("start:app", host="0.0.0.0", port=1111)
