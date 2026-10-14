from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_details.model import ProductDetail


class AbstractProductDetailRepository(ABC):
    @abstractmethod
    async def create(
        self,
        detail: ProductDetail,
    ) -> ProductDetail: ...

    @abstractmethod
    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> ProductDetail | None: ...

    @abstractmethod
    async def update(
        self,
        detail: ProductDetail,
    ) -> ProductDetail: ...

    @abstractmethod
    async def delete(
        self,
        detail: ProductDetail,
    ) -> None: ...
