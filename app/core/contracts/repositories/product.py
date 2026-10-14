from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.products.dtos import (
    ProductQueryDTO,
    PublicProductListResult,
    PublicProductQueryDTO,
)
from app.modules.products.model import Product
from app.modules.products.query import ProductListResult


class AbstractProductRepository(ABC):
    @abstractmethod
    async def get_public_by_id(
        self,
        product_id: UUID,
    ) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def list_public(
        self,
        *,
        query: PublicProductQueryDTO,
    ) -> PublicProductListResult:
        raise NotImplementedError

    @abstractmethod
    async def list_featured(
        self,
        *,
        page: int,
        page_size: int,
    ) -> ProductListResult:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        product_id: UUID,
    ) -> Product | None:
        raise NotImplementedError

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
        query: ProductQueryDTO,
    ) -> ProductListResult:
        raise NotImplementedError

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
    async def create(
        self,
        product: Product,
    ) -> Product: ...

    @abstractmethod
    async def delete(
        self,
        product: Product,
    ) -> None: ...
