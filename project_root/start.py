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
from app.api.services import api_key, follower, tweet, user
from tests import data_aggregate


@asynccontextmanager
async def lifespan(*_: FastAPI):
    """Эта функция будет вызвана при запуске приложения
    и она будет использоваться для инициализации базы данных"""
    users, api_keys, tweets, media = await data_aggregate.main()
    parse_tweets, list_tweets = tweets

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with manager.get_session() as session:
        for user_obj in users:
            tweet_obj = parse_tweets.pop()
            user_flush = await user.create_user_flush(user_obj, session)
            await api_key.save_user_api_key(api_keys.pop(), user_flush, session)
            list_tweets_flush = await tweet.create_tweets_flush(tweet_obj, session)
            await tweet.save_user_tweets_with_likes_and_media(
                list_tweets_flush, user_flush, media, session
            )

        await follower.save_user_followers(session)
        await conn.commit()

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
app = FastAPI(title=project_name, version=project_version, lifespan=lifespan)
app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory="app/api/static", html=True), name="static")
app.add_middleware(DBSessionMiddleware, session_manager=manager)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("start:app", host="0.0.0.0", port=1111)
