from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.collections.model import Collection


class AbstractCollectionRepository(ABC):
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
    async def list(
        self,
        brand_id: UUID,
        *,
        status: RecordStatus | None = None,
    ) -> list[Collection]: ...

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
