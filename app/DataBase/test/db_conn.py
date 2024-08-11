from sqlalchemy.ext.asyncio import create_async_engine
from cfg import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)
