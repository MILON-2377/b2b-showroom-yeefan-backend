from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.catalogs.dtos import (
    AdminCatalogListDTO,
    AdminCatalogQueryDTO,
    CatalogDTO,
    CreateCatalogDTO,
    PublicCatalogDTO,
    PublicCatalogListDTO,
    PublicCatalogQueryDTO,
    UpdateCatalogDTO,
)


class AbstractCatalogService(ABC):
    @abstractmethod
    async def list_admin(
        self,
        query: AdminCatalogQueryDTO,
    ) -> AdminCatalogListDTO:
        raise NotImplementedError

    @abstractmethod
    async def list_public(
        self,
        query: PublicCatalogQueryDTO,
    ) -> PublicCatalogListDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_public_by_collection_id(
        self,
        collection_id: UUID,
    ) -> CatalogDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        catalog_id: UUID,
    ) -> CatalogDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_collection_id(
        self,
        collection_id: UUID,
    ) -> PublicCatalogDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        payload: CreateCatalogDTO,
    ) -> CatalogDTO:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        catalog_id: UUID,
        payload: UpdateCatalogDTO,
    ) -> CatalogDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        catalog_id: UUID,
    ) -> None:
        raise NotImplementedError
