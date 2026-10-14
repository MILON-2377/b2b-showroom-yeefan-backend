from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.catalogs.model import Catalog
from app.modules.media.model import MediaAsset


class AbstractCatalogRepository(ABC):
    @abstractmethod
    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        collection_id: UUID | None = None,
        status: RecordStatus | None = None,
        sort_order: str = "desc",
    ) -> tuple[
        list[tuple[Catalog, MediaAsset, MediaAsset]],
        int,
    ]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, catalog_id: UUID) -> Catalog | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_collection_id(
        self,
        collection_id: UUID,
    ) -> Catalog | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, catalog: Catalog) -> Catalog:
        raise NotImplementedError

    @abstractmethod
    async def update(self, catalog: Catalog) -> Catalog:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, catalog: Catalog) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        collection_id: UUID | None = None,
        sort_order: str = "desc",
    ) -> tuple[list[tuple[Catalog, MediaAsset, MediaAsset]], int]:
        raise NotImplementedError
