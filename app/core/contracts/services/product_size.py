from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_sizes.dtos.product_size import (
    CreateProductSizeWithMeasurementDTO,
    ProductSizeDTO,
    UpdateProductSizeDTO,
)


class AbstractProductSizeService(ABC):
    @abstractmethod
    async def create_many(
        self,
        *,
        product_id: UUID,
        payloads: tuple[CreateProductSizeWithMeasurementDTO, ...],
    ) -> list[ProductSizeDTO]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        *,
        product_id: UUID,
        name: str,
        sort_order: int = 0,
    ) -> ProductSizeDTO:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        *,
        size_id: UUID,
    ) -> ProductSizeDTO:
        raise NotImplementedError

    @abstractmethod
    async def list_by_product(
        self,
        *,
        product_id: UUID,
    ) -> list[ProductSizeDTO]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        *,
        size_id: UUID,
        name: str,
        sort_order: int,
    ) -> ProductSizeDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        *,
        size_id: UUID,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_many(
        self,
        *,
        product_id: UUID,
        payloads: tuple[UpdateProductSizeDTO, ...],
    ) -> list[ProductSizeDTO]:
        raise NotImplementedError
