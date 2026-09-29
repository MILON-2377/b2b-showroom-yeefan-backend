from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.collection import (
    AbstractCollectionRepository,
)
from app.core.models import RecordStatus
from app.modules.collections.model import Collection


class CollectionRepository(AbstractCollectionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

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

    async def list(
        self,
        brand_id: UUID,
        *,
        status: RecordStatus | None = None,
    ) -> list[Collection]:
        statement = (
            select(Collection)
            .where(Collection.brand_id == brand_id)
            .order_by(Collection.name)
        )

        if status is not None:
            statement = statement.where(Collection.status == status)

        result = await self.session.execute(statement)
        return list(result.scalars().all())

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
