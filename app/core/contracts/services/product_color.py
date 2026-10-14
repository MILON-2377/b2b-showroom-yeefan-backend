from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_colors.dtos import (
    CreateProductColorDTO,
    ProductColorDTO,
    UpdateProductColorDTO,
)


class AbstractProductColorService(ABC):
    @abstractmethod
    async def create_many(
        self,
        *,
        product_id: UUID,
        payloads: list[CreateProductColorDTO],
    ) -> list[ProductColorDTO]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        *,
        product_id: UUID,
        name: str,
        sort_order: int = 0,
    ) -> ProductColorDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        *,
        color_id: UUID,
    ) -> ProductColorDTO:
        raise NotImplementedError

    @abstractmethod
    async def list_by_product(
        self,
        *,
        product_id: UUID,
    ) -> list[ProductColorDTO]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        *,
        color_id: UUID,
        name: str,
        sort_order: int,
    ) -> ProductColorDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        *,
        color_id: UUID,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_many(
        self, *, product_id: UUID, payloads: tuple[UpdateProductColorDTO, ...]
    ) -> list[ProductColorDTO]:
        raise NotImplementedError
