from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.db.db import engine
from app.api.db.base_models import Base
from app.api.core.settings import Settings
from app.api.router.router import api_router


@asynccontextmanager
async def lifespan(*_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

settings = Settings()
project_name = settings.project_name
project_version = settings.project_version
app = FastAPI(title=project_name, version=project_version, lifespan=lifespan)
app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory="app/api/static", html=True), name="static")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("start:app", host="0.0.0.0", port=1111)
