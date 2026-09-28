from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import AsyncSessionLocal


class UnitOfWork:
    def __init__(self, session: AsyncSession):

        self.session = session

    async def flush(self):
        await self.session.flush()

    async def refresh(self, entity):
        await self.session.refresh(entity)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):

        if not self.session.in_transaction():
            await self.session.begin()

        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                await self.rollback()

        finally:
            await self.session.close()
