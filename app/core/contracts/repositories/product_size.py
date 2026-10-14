from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_sizes.models.product_size import ProductSize


class AbstractProductSizeRepository(ABC):
    @abstractmethod
    async def create_many(
        self,
        sizes: list[ProductSize],
    ) -> list[ProductSize]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        size: ProductSize,
    ) -> ProductSize:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        size_id: UUID,
    ) -> ProductSize | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> list[ProductSize]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        size: ProductSize,
    ) -> ProductSize:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        size: ProductSize,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_many(
        self,
        sizes: list[ProductSize],
    ) -> list[ProductSize]:
        raise NotImplementedError

    @abstractmethod
    async def delete_many(
        self,
        sizes: list[ProductSize],
    ) -> None:
        raise NotImplementedError
