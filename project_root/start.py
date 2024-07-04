from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.core.settings import Settings
from app.api.db.base_models import Base
from app.api.db.db import async_engine, get_session
from app.api.router.router import api_router
from app.api.services import user, api_key, follower, tweet, like
from tests import data_aggregate


@asynccontextmanager
async def lifespan(*_: FastAPI):
    users, api_keys, followers, tweets = await data_aggregate.main()
    parse_tweets, list_tweets = tweets
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with get_session() as session:
        for user_obj in users:
            tweet_obj = parse_tweets.pop()
            user_flush = await user.create_user_flush(user_obj, session)
            await api_key.save_user_api_key(api_keys.pop(), user_flush, session)
            await follower.save_user_followers(followers.pop(), user_flush, session)
            await like.save_user_likes(list_tweets, user_flush, session)
            await tweet.save_user_tweets(tweet_obj, user_flush, session)
            await conn.commit()

    yield
    await async_engine.dispose()


settings = Settings()
project_name = settings.project_name
project_version = settings.project_version
app = FastAPI(title=project_name, version=project_version, lifespan=lifespan)
app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory="app/api/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("start:app", host="0.0.0.0", port=1111)
