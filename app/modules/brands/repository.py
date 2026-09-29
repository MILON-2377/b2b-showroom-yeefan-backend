from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.brand import AbstractBrandRepository
from app.core.models import RecordStatus

from .model import Brand


class BrandRepository(AbstractBrandRepository):
    def __init__(self, session: AsyncSession):

        self.session = session

    async def get_by_id(self, brand_id: UUID) -> Brand | None:

        statement = select(Brand).where(Brand.id == brand_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Brand | None:

        result = await self.session.execute(select(Brand).where(Brand.slug == slug))

        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        status: RecordStatus | None = None,
    ) -> list[Brand]:

        statement = select(Brand).order_by(Brand.name)

        if status is not None:
            statement = statement.where(Brand.status == status)

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def exists_by_slug(
        self, slug: str, *, exclude_id: UUID | None = None
    ) -> bool:

        statement = select(Brand.id).where(Brand.slug == slug)

        if exclude_id is not None:
            statement = statement.where(Brand.id != exclude_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def add(self, brand: Brand) -> Brand:

        self.session.add(brand)

        return brand

    async def delete(self, brand: Brand) -> None:
        await self.session.delete(brand)
