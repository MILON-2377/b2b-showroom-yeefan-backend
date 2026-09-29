from uuid import UUID

from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.collections.model import Collection
from app.shared.utils.slug import create_slug


class CollectionService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create(
        self,
        *,
        brand_id: UUID,
        name: str,
        description: str | None = None,
        cover_media_url: str | None = None,
        status: RecordStatus = RecordStatus.DRAFT,
    ) -> Collection:
        # The collection must belong to an existing brand.
        brand = await self.uow.brands.get_by_id(brand_id)

        if brand is None:
            raise ValueError(f"Brand '{brand_id}' not found")

        slug = create_slug(name)

        if await self.uow.collections.exists_by_slug(
            brand_id,
            slug,
        ):
            raise ValueError(
                f"Collection slug '{slug}' already exists for brand '{brand_id}'"
            )

        collection = Collection(
            brand_id=brand_id,
            name=name,
            slug=slug,
            description=description,
            cover_media_url=cover_media_url,
            status=status,
        )

        await self.uow.collections.add(collection)
        await self.uow.commit()

        return collection

    async def get_by_id(
        self,
        collection_id: UUID,
    ) -> Collection | None:
        return await self.uow.collections.get_by_id(collection_id)

    async def get_by_slug(
        self,
        brand_id: UUID,
        slug: str,
    ) -> Collection | None:
        return await self.uow.collections.get_by_slug(
            brand_id,
            slug,
        )

    async def list(
        self,
        brand_id: UUID,
        *,
        status: RecordStatus | None = None,
    ) -> list[Collection]:
        return await self.uow.collections.list(
            brand_id,
            status=status,
        )

    async def delete(
        self,
        collection_id: UUID,
    ) -> None:
        collection = await self.uow.collections.get_by_id(collection_id)

        if collection is None:
            raise ValueError(f"Collection '{collection_id}' not found")

        await self.uow.collections.delete(collection)
        await self.uow.commit()
