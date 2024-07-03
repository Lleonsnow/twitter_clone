from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.api.core.settings import Settings

settings = Settings()
# DATABASE_URL = settings.base_url.get_secret_value()
DATABASE_URL = settings.db_test.get_secret_value()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with async_session() as session:
        yield session
