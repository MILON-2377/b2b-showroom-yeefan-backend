from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_media.dtos import (
    CreateProductMediaDTO,
    ProductMediaDTO,
    UpdateProductMediaDTO,
)


class AbstractProductMediaService(ABC):
    @abstractmethod
    async def create_many(
        self,
        *,
        product_id: UUID,
        payloads: list[CreateProductMediaDTO],
    ) -> list[ProductMediaDTO]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        *,
        product_id: UUID,
        media_asset_id: UUID,
        alt_text: str | None = None,
        sort_order: int = 0,
        is_primary: bool = False,
    ) -> ProductMediaDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        product_media_id: UUID,
    ) -> ProductMediaDTO:
        raise NotImplementedError

    @abstractmethod
    async def list_by_product(
        self,
        product_id: UUID,
    ) -> list[ProductMediaDTO]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        product_media_id: UUID,
        *,
        alt_text: str | None,
        sort_order: int,
        is_primary: bool,
    ) -> ProductMediaDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_many(
        self,
        product_id: UUID,
        payloads: tuple[UpdateProductMediaDTO, ...],
    ) -> list[ProductMediaDTO]:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        product_media_id: UUID,
    ) -> None:
        raise NotImplementedError
