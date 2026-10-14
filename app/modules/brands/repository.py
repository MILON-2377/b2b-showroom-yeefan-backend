from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.brand import AbstractBrandRepository
from app.core.models import RecordStatus

from .model import Brand
from .query import BrandListQuery, BrandListResult


class BrandRepository(AbstractBrandRepository):
    def __init__(self, session: AsyncSession):

        self.session = session

    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[Brand], int]:
        filters = [
            Brand.status == RecordStatus.PUBLISHED,
        ]

        if search:
            pattern = f"%{search.strip()}%"

            filters.append(
                or_(
                    Brand.name.ilike(pattern),
                    Brand.description.ilike(pattern),
                )
            )

        count_statement = select(func.count(Brand.id)).where(*filters)

        total = await self.session.scalar(count_statement) or 0

        statement = (
            select(Brand)
            .where(*filters)
            .order_by(
                Brand.created_at.desc(),
                Brand.id.asc(),
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all()), total

    async def get_by_id(self, brand_id: UUID) -> Brand | None:

        statement = select(Brand).where(Brand.id == brand_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Brand | None:

        result = await self.session.execute(select(Brand).where(Brand.slug == slug))

        return result.scalar_one_or_none()

    async def list(self, query: BrandListQuery) -> BrandListResult:

        filters = []

        if query.status is not None:
            filters.append(Brand.status == query.status)

        if query.search:
            search = f"%{query.search}%"
            filters.append(Brand.name.ilike(search))

        count_statement = select(func.count()).select_from(Brand).where(*filters)

        total = await self.session.scalar(count_statement)

        offset = (query.page - 1) * query.page_size

        statement = (
            select(Brand)
            .where(*filters)
            .order_by(Brand.name)
            .offset(offset)
            .limit(query.page_size)
        )

        result = await self.session.execute(statement)

        return BrandListResult(
            items=list(result.scalars().all()),
            total=total or 0,
        )

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

    async def update(self, brand: Brand) -> Brand:
        self.session.add(brand)
        return brand
