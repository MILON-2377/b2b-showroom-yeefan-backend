from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .connection import engine

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
