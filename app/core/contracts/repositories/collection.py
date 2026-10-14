from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.collections.model import Collection
from app.modules.collections.query import CollectionListQuery, CollectionListResult


class AbstractCollectionRepository(ABC):
    @abstractmethod
    async def list_public(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> list[Collection]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        collection_id: UUID,
    ) -> Collection | None: ...

    @abstractmethod
    async def get_by_slug(
        self,
        brand_id: UUID,
        slug: str,
    ) -> Collection | None: ...

    @abstractmethod
    async def list(self, query: CollectionListQuery) -> CollectionListResult: ...

    @abstractmethod
    async def exists_by_slug(
        self,
        brand_id: UUID,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool: ...

    @abstractmethod
    async def add(
        self,
        collection: Collection,
    ) -> Collection: ...

    @abstractmethod
    async def delete(
        self,
        collection: Collection,
    ) -> None: ...

    @abstractmethod
    async def update(self, collection: Collection) -> Collection: ...

    @abstractmethod
    async def exists_by_brand_id(
        self,
        brand_id: UUID,
    ) -> bool: ...
