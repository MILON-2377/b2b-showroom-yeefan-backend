from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_colors.model import ProductColor


class AbstractProductColorRepository(ABC):
    @abstractmethod
    async def create_many(
        self,
        colors: list[ProductColor],
    ) -> list[ProductColor]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        color: ProductColor,
    ) -> ProductColor:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        color_id: UUID,
    ) -> ProductColor | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> list[ProductColor]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        color: ProductColor,
    ) -> ProductColor:
        raise NotImplementedError

    @abstractmethod
    async def update_many(
        self,
        colors: list[ProductColor],
    ) -> list[ProductColor]:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        color: ProductColor,
    ) -> None:
        raise NotImplementedError


    @abstractmethod
    async def delete_many(
        self,
        colors: list[ProductColor],
    ) -> None:
        raise NotImplementedError