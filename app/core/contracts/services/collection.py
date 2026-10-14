from abc import ABC, abstractmethod
from uuid import UUID

from app.core.database.models import Collection
from app.modules.collections.dtos import (
    CollectionDTO,
    PublicCollectionListDTO,
    PublicCollectionQueryDTO,
)
from app.modules.collections.query import (
    CollectionListQuery,
    CollectionListResult,
)


class AbstractCollectionService(ABC):
    @abstractmethod
    async def list_public(
        self,
        query: PublicCollectionQueryDTO,
    ) -> PublicCollectionListDTO:
        raise NotImplementedError

    @abstractmethod
    async def validate_for_product(
        self,
        *,
        collection_id: UUID,
        brand_id: UUID,
    ) -> CollectionDTO: ...

    @abstractmethod
    async def create(
        self,
        *,
        brand_id: UUID,
        name: str,
        description: str | None = None,
        cover_media_url: str | None = None,
    ) -> Collection: ...

    @abstractmethod
    async def get_by_id(
        self,
        collection_id: UUID,
    ) -> Collection: ...

    @abstractmethod
    async def list(
        self,
        query: CollectionListQuery,
    ) -> CollectionListResult: ...

    @abstractmethod
    async def update(
        self,
        collection_id: UUID,
        *,
        name: str,
        description: str | None = None,
        cover_media_url: str | None = None,
    ) -> Collection: ...

    @abstractmethod
    async def delete(
        self,
        collection_id: UUID,
    ) -> None: ...
