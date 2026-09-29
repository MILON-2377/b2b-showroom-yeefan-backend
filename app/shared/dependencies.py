from collections.abc import AsyncGenerator

from app.core.database.session import AsyncSessionLocal
from app.core.database.unit_of_work import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with AsyncSessionLocal() as session:
        async with UnitOfWork(session) as uow:
            yield uow
