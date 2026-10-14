from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.product_colors.dtos import (
    CreateProductColorDTO,
    ProductColorDTO,
    UpdateProductColorDTO,
)
from app.modules.product_customizations.dtos.product_customization import (
    CreateProductCustomizationDTO,
    ProductCustomizationDTO,
    UpdateProductCustomizationDTO,
)
from app.modules.product_details.dtos import (
    CreateProductDetailDTO,
    ProductDetailDTO,
    UpdateProductDetailDTO,
)
from app.modules.product_media.dtos import (
    CreateProductMediaDTO,
    ProductMediaDTO,
    UpdateProductMediaDTO,
)
from app.modules.product_sizes.dtos.product_measurement_guide import (
    CreateProductMeasurementGuideDTO,
    ProductMeasurementGuideDTO,
    UpdateProductMeasurementGuideDTO,
)
from app.modules.product_sizes.dtos.product_size import (
    CreateProductSizeDTO,
    ProductSizeDTO,
    UpdateProductSizeDTO,
)

if TYPE_CHECKING:
    from app.modules.products.model import Product


@dataclass(frozen=True)
class ProductDTO:
    id: UUID
    brand_id: UUID
    collection_id: UUID
    category_id: UUID
    product_code: str
    slug: str
    name: str
    description: str | None
    status: RecordStatus
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

    media: tuple[ProductMediaDTO, ...]
    details: ProductDetailDTO | None
    colors: tuple[ProductColorDTO, ...]
    sizes: tuple[ProductSizeDTO, ...]
    measurement_guide: ProductMeasurementGuideDTO | None
    customization: ProductCustomizationDTO | None


@dataclass(frozen=True)
class CreateProductDTO:
    brand_id: UUID
    collection_id: UUID
    category_id: UUID

    name: str
    description: str | None = None

    media: tuple[CreateProductMediaDTO, ...] = ()
    details: CreateProductDetailDTO | None = None
    colors: tuple[CreateProductColorDTO, ...] = ()
    sizes: tuple[CreateProductSizeDTO, ...] = ()
    measurement_guide: CreateProductMeasurementGuideDTO | None = None
    customization: CreateProductCustomizationDTO | None = None


@dataclass(frozen=True)
class ProductQueryDTO:
    search: str | None = None

    status: RecordStatus | None = None

    brand_id: UUID | None = None
    collection_id: UUID | None = None
    category_id: UUID | None = None

    page: int = 1
    page_size: int = 20

    sort_by: str = "created_at"
    sort_order: str = "desc"


@dataclass(frozen=True)
class PaginationDTO:
    page: int
    page_size: int
    total: int
    total_pages: int


@dataclass(frozen=True)
class ProductListImageDTO:
    id: UUID
    url: str
    mime_type: str | None
    width: int | None
    height: int | None


@dataclass(frozen=True)
class ProductListItem:
    id: UUID
    product_code: str
    name: str
    slug: str

    description: str | None
    status: RecordStatus

    brand_id: UUID
    collection_id: UUID
    category_id: UUID

    image: ProductListImageDTO | None

    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ProductListResult:
    items: list[ProductListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass(frozen=True)
class ProductListResultDTO:
    items: list[ProductListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass(frozen=True)
class ProductMediaQueryDTO:
    id: UUID
    media_asset_id: UUID
    alt_text: str | None
    url: str
    mime_type: str | None
    width: int | None
    height: int | None
    sort_order: int
    is_primary: bool


@dataclass(frozen=True)
class ProductDetailQueryDTO:
    id: UUID
    brand_id: UUID
    collection_id: UUID
    category_id: UUID
    product_code: str
    name: str
    slug: str
    description: str | None
    status: RecordStatus
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

    media: list[ProductMediaQueryDTO]
    details: ProductDetailDTO | None
    colors: list[ProductColorDTO]
    sizes: list[ProductSizeDTO]
    measurement_guide: ProductMeasurementGuideDTO | None
    customization: ProductCustomizationDTO | None


UNSET = object()


@dataclass(frozen=True)
class UpdateProductDTO:
    name: str | None | Any = UNSET
    description: str | None | Any = UNSET

    brand_id: UUID | None | Any = UNSET
    collection_id: UUID | None | Any = UNSET
    category_id: UUID | None | Any = UNSET

    status: RecordStatus | None | Any = UNSET

    media: tuple[UpdateProductMediaDTO, ...] | None | Any = UNSET
    details: UpdateProductDetailDTO | None | Any = UNSET
    colors: tuple[UpdateProductColorDTO, ...] | None | Any = UNSET
    sizes: tuple[UpdateProductSizeDTO, ...] | None | Any = UNSET
    measurement_guide: UpdateProductMeasurementGuideDTO | None | Any = UNSET
    customization: UpdateProductCustomizationDTO | None | Any = UNSET


# Publics
@dataclass(frozen=True)
class PublicFeaturedProductDTO:
    id: UUID
    product_code: str
    name: str
    slug: str
    description: str | None
    image_id: UUID | None
    image_url: str | None


@dataclass(frozen=True)
class PublicFeaturedProductListDTO:
    items: tuple[PublicFeaturedProductDTO, ...]
    total: int


class ProductSortBy(StrEnum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
    PRODUCT_CODE = "product_code"


class ProductSortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True)
class ProductCursor:
    sort_by: ProductSortBy
    sort_order: ProductSortOrder
    value: str
    product_id: UUID


@dataclass(frozen=True)
class PublicProductQueryDTO:
    cursor: str | None = None
    page_size: int = 20

    search: str | None = None

    brand_id: UUID | None = None
    collection_id: UUID | None = None
    category_id: UUID | None = None

    sort_by: ProductSortBy = ProductSortBy.CREATED_AT
    sort_order: ProductSortOrder = ProductSortOrder.DESC


@dataclass(frozen=True)
class PublicProductListResult:
    items: tuple["Product", ...]
    next_cursor: str | None
    has_more: bool



@dataclass(frozen=True)
class PublicProductMediaDTO:
    id: UUID
    url: str


@dataclass(frozen=True)
class PublicProductDTO:
    id: UUID
    product_code: str
    name: str
    slug: str
    description: str | None
    media: tuple[PublicProductMediaDTO, ...]