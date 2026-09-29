from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.database_url, echo=True, pool_pre_ping=True, pool_recycle=300
)
