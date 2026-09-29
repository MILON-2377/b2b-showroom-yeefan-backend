from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_media.model import ProductMedia


class AbstractProductMediaRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        product_media_id: UUID,
    ) -> ProductMedia | None: ...

    @abstractmethod
    async def list_by_product(
        self,
        product_id: UUID,
    ) -> list[ProductMedia]: ...

    @abstractmethod
    async def add(
        self,
        product_media: ProductMedia,
    ) -> ProductMedia: ...

    @abstractmethod
    async def delete(
        self,
        product_media: ProductMedia,
    ) -> None: ...
