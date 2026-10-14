from uuid import UUID

from sqlalchemy import exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.collection import (
    AbstractCollectionRepository,
)
from app.core.models import RecordStatus
from app.modules.collections.model import Collection

from .query import CollectionListQuery, CollectionListResult


class CollectionRepository(AbstractCollectionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_public(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[Collection], int]:

        filters = [
            Collection.status == RecordStatus.PUBLISHED,
        ]

        if search:
            pattern = f"%{search.strip()}%"

            filters.append(
                or_(
                    Collection.name.ilike(pattern),
                    Collection.description.ilike(pattern),
                )
            )

        count_statement = select(func.count(Collection.id)).where(*filters)

        total = await self.session.scalar(count_statement) or 0

        statement = (
            select(Collection)
            .where(*filters)
            .order_by(
                Collection.created_at.desc(),
                Collection.id.asc(),
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all()), total

    async def get_by_id(
        self,
        collection_id: UUID,
    ) -> Collection | None:
        result = await self.session.execute(
            select(Collection).where(Collection.id == collection_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        brand_id: UUID,
        slug: str,
    ) -> Collection | None:
        result = await self.session.execute(
            select(Collection).where(
                Collection.brand_id == brand_id,
                Collection.slug == slug,
            )
        )
        return result.scalar_one_or_none()

    async def list(self, query: CollectionListQuery) -> CollectionListResult:

        filters = []

        if query.brand_id is not None:
            filters.append(Collection.brand_id == query.brand_id)

        if query.status is not None:
            filters.append(Collection.status == query.status)

        if query.search:
            search = f"%{query.search}"

            filters.append(Collection.name.ilike(search))

        count_statement = select(func.count()).select_from(Collection).where(*filters)

        total = await self.session.scalar(count_statement)

        offset = (query.page - 1) * query.page_size

        statement = (
            select(Collection)
            .where(*filters)
            .order_by(Collection.name)
            .offset(offset)
            .limit(query.page_size)
        )

        result = await self.session.execute(statement)

        return CollectionListResult(
            items=list(result.scalars().all()), total=total or 0
        )

    async def exists_by_slug(
        self,
        brand_id: UUID,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool:
        statement = select(Collection.id).where(
            Collection.brand_id == brand_id,
            Collection.slug == slug,
        )

        if exclude_id is not None:
            statement = statement.where(Collection.id != exclude_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def add(
        self,
        collection: Collection,
    ) -> Collection:
        self.session.add(collection)
        return collection

    async def delete(
        self,
        collection: Collection,
    ) -> None:
        await self.session.delete(collection)

    async def update(self, collection: Collection) -> Collection:

        self.session.add(collection)

        return collection

    async def exists_by_brand_id(self, brand_id: UUID) -> bool:
        statement = select(exists().where(Collection.brand_id == brand_id))

        return bool(await self.session.scalar(statement))
