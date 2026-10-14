from collections.abc import AsyncGenerator

from app.core.database.session import AsyncSessionLocal
from app.core.database.unit_of_work import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    session = AsyncSessionLocal()

    async with UnitOfWork(session=session) as uow:
        yield uow
