from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_media.model import ProductMedia


class AbstractProductMediaRepository(ABC):
    @abstractmethod
    async def create_many(
        self,
        product_media: list[ProductMedia],
    ) -> list[ProductMedia]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        product_media: ProductMedia,
    ) -> ProductMedia:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        product_media_id: UUID,
    ) -> ProductMedia | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> list[ProductMedia]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        product_media: ProductMedia,
    ) -> ProductMedia:
        raise NotImplementedError

    @abstractmethod
    async def update_many(
        self,
        product_media: list[ProductMedia],
    ) -> list[ProductMedia]:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        product_media: ProductMedia,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_many(
        self,
        product_media: list[ProductMedia],
    ) -> None:
        raise NotImplementedError
