from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.products.dtos import (
    CreateProductDTO,
    ProductDetailQueryDTO,
    ProductDTO,
    ProductListResultDTO,
    ProductQueryDTO,
    PublicFeaturedProductListDTO,
    PublicProductListResult,
    PublicProductQueryDTO,
    UpdateProductDTO,
)
from app.modules.products.schemas import CreateProductRequest


class AbstractProductService(ABC):
    @abstractmethod
    async def get_public_by_id(
        self,
        product_id: UUID,
    ) -> ProductDetailQueryDTO:
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
    ) -> PublicFeaturedProductListDTO:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        *,
        product_id: UUID,
        payload: UpdateProductDTO,
    ) -> ProductDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        product_id: UUID,
    ) -> ProductDetailQueryDTO:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        *,
        query: ProductQueryDTO,
    ) -> ProductListResultDTO:
        raise NotImplementedError

    @abstractmethod
    async def validate_product_code(
        self,
        *,
        brand_id: UUID,
        product_code: str,
    ) -> None: ...

    @abstractmethod
    async def validate_slug(
        self,
        *,
        brand_id: UUID,
        slug: str,
        exclude_id: UUID | None = None,
    ) -> None: ...

    @abstractmethod
    async def create(
        self,
        *,
        payload: CreateProductDTO,
    ) -> ProductDTO: ...

    @staticmethod
    @abstractmethod
    def _to_create_product_dto(
        payload: CreateProductRequest,
    ) -> CreateProductDTO: ...
