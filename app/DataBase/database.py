from sqlalchemy.ext.asyncio import create_async_engine
from app.DataBase.config import settings


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
    # pool_size=5,
    # max_overflow=10,
)
