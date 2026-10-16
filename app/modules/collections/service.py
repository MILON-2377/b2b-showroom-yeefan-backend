import math
from uuid import UUID

from app.core.contracts.services.collection import AbstractCollectionService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.errors.base import (
    BrandNotFoundError,
    CollectionNotFoundError,
    CollectionSlugAlreadyExistsError,
)
from app.core.models import RecordStatus
from app.modules.collections.dtos import (
    AvailableCatalogCollectionsDTO,
    CollectionDTO,
    PublicCollectionListDTO,
    PublicCollectionQueryDTO,
)
from app.modules.collections.model import Collection
from app.shared.utils.slug import create_slug

from .query import CollectionListQuery, CollectionListResult


class CollectionService(AbstractCollectionService):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def list_public(
        self,
        query: PublicCollectionQueryDTO,
    ) -> PublicCollectionListDTO:
        collections, total = await self.uow.collections.list_public(
            page=query.page,
            page_size=query.page_size,
            search=query.search,
        )

        items = [self._to_dto(collection) for collection in collections]

        return PublicCollectionListDTO(
            items=items,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=math.ceil(total / query.page_size) if total else 0,
        )

    async def create(
        self,
        *,
        brand_id: UUID,
        name: str,
        description: str | None = None,
        cover_media_url: str | None = None,
        status: RecordStatus = RecordStatus.DRAFT,
    ) -> Collection:
        brand = await self.uow.brands.get_by_id(brand_id)

        if brand is None:
            raise BrandNotFoundError(brand_id)

        slug = create_slug(name)

        exists = await self.uow.collections.exists_by_slug(
            brand_id,
            slug,
        )

        if exists:
            raise CollectionSlugAlreadyExistsError(slug)

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
    ) -> Collection:
        collection = await self.uow.collections.get_by_id(collection_id)

        if collection is None:
            raise CollectionNotFoundError(collection_id)

        return collection

    async def get_by_slug(
        self,
        brand_id: UUID,
        slug: str,
    ) -> Collection | None:
        return await self.uow.collections.get_by_slug(
            brand_id,
            slug,
        )

    async def list(self, query: CollectionListQuery) -> CollectionListResult:
        return await self.uow.collections.list(query)

    async def delete(
        self,
        collection_id: UUID,
    ) -> None:
        collection = await self.uow.collections.get_by_id(collection_id)

        if collection is None:
            raise ValueError(f"Collection '{collection_id}' not found")

        await self.uow.collections.delete(collection)
        await self.uow.commit()

    async def update(
        self,
        collection_id: UUID,
        name: str,
        description: str | None = None,
        cover_media_url: str | None = None,
        status: RecordStatus | None = None,
    ) -> Collection:

        collection = await self.uow.collections.get_by_id(collection_id)

        if collection is None:
            raise CollectionNotFoundError(collection_id)

        slug = create_slug(name)

        if slug != collection.slug:
            exists = await self.uow.collections.exists_by_slug(
                collection.brand_id,
                slug,
                exclude_id=collection_id,
            )

            if exists:
                raise CollectionSlugAlreadyExistsError(slug)

        collection.name = name
        collection.slug = slug
        collection.description = description
        collection.cover_media_url = cover_media_url

        if status is not None:
            collection.status = status

        await self.uow.collections.update(collection)

        await self.uow.commit()

        await self.uow.refresh(collection)

        return collection

    async def list_by_unused_catalogs(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> AvailableCatalogCollectionsDTO:

        collections, total = await self.uow.collections.list_by_unused_catalogs(
            page=page,
            page_size=page_size,
            search=search,
        )

        return AvailableCatalogCollectionsDTO(
            items=[self._to_dto(collection) for collection in collections],
            total=total,
            page=page,
            page_size=page_size,
        )

    # Validation
    async def validate_for_product(
        self,
        *,
        collection_id: UUID,
    ) -> CollectionDTO:
        collection = await self.uow.collections.get_by_id(collection_id)

        if collection is None:
            raise CollectionNotFoundError(collection_id)

        return self._to_dto(collection)

    @staticmethod
    def _to_dto(collection: Collection) -> CollectionDTO:
        return CollectionDTO(
            id=collection.id,
            brand_id=collection.brand_id,
            name=collection.name,
            slug=collection.slug,
            description=collection.description,
            status=collection.status,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
        )
