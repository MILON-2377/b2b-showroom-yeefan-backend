from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.products.model import Product


class AbstractProductRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        product_id: UUID,
    ) -> Product | None: ...

    @abstractmethod
    async def get_by_slug(
        self,
        brand_id: UUID,
        slug: str,
    ) -> Product | None: ...

    @abstractmethod
    async def get_by_product_code(
        self,
        brand_id: UUID,
        product_code: str,
    ) -> Product | None: ...

    @abstractmethod
    async def list(
        self,
        *,
        brand_id: UUID | None = None,
        collection_id: UUID | None = None,
        category_id: UUID | None = None,
        status: RecordStatus | None = None,
    ) -> list[Product]: ...

    @abstractmethod
    async def exists_by_slug(
        self,
        brand_id: UUID,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool: ...

    @abstractmethod
    async def exists_by_product_code(
        self,
        brand_id: UUID,
        product_code: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool: ...

    @abstractmethod
    async def add(
        self,
        product: Product,
    ) -> Product: ...

    @abstractmethod
    async def delete(
        self,
        product: Product,
    ) -> None: ...
