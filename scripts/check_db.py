import asyncio

from sqlalchemy import text

from app.core.database.session import AsyncSessionLocal


async def check_database() -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        print(result.scalar_one())


if __name__ == "__main__":
    asyncio.run(check_database())
