from datetime import datetime
from enum import Enum
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.core.models import RecordStatus
from app.modules.product_colors.schemas import (
    CreateProductColorRequest,
    ProductColorResponse,
    UpdateProductColorRequest,
)
from app.modules.product_customizations.schemas import (
    CreateProductCustomizationRequest,
    ProductCustomizationResponse,
    UpdateProductCustomizationRequest,
)
from app.modules.product_details.schemas import (
    CreateProductDetailRequest,
    ProductDetailResponse,
    UpdateProductDetailRequest,
)
from app.modules.product_media.schemas import (
    CreateProductMediaRequest,
    ProductMediaQueryResponse,
    ProductMediaResponse,
    UpdateProductMediaRequest,
)
from app.modules.product_sizes.schemas import (
    CreateProductMeasurementGuideRequest,
    CreateProductSizeRequest,
    ProductMeasurementGuideResponse,
    ProductSizeResponse,
    UpdateProductMeasurementGuideRequest,
    UpdateProductSizeRequest,
)
from app.modules.products.dtos import (
    ProductDetailQueryDTO,
    ProductDTO,
    ProductListResultDTO,
    ProductSortBy,
    ProductSortOrder,
    PublicFeaturedProductDTO,
    PublicProductDTO,
    PublicProductQueryDTO,
)


class CreateProductRequest(BaseModel):
    brand_id: UUID
    collection_id: UUID
    category_id: UUID

    name: str = Field(min_length=1, max_length=255)
    description: str | None = None

    media: list["CreateProductMediaRequest"] = Field(default_factory=list)
    details: "CreateProductDetailRequest | None" = None
    colors: list["CreateProductColorRequest"] = Field(default_factory=list)
    sizes: list["CreateProductSizeRequest"] = Field(default_factory=list)
    measurement_guide: "CreateProductMeasurementGuideRequest | None" = None
    customization: "CreateProductCustomizationRequest | None" = None


class ProductResponse(BaseModel):
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

    media: list[ProductMediaResponse]
    details: ProductDetailResponse | None
    colors: list[ProductColorResponse]
    sizes: list[ProductSizeResponse]
    measurement_guide: ProductMeasurementGuideResponse | None
    customization: ProductCustomizationResponse | None

    @classmethod
    def from_dto(
        cls,
        dto: ProductDTO,
    ) -> Self:
        return cls(
            id=dto.id,
            brand_id=dto.brand_id,
            collection_id=dto.collection_id,
            category_id=dto.category_id,
            product_code=dto.product_code,
            name=dto.name,
            slug=dto.slug,
            description=dto.description,
            status=dto.status,
            published_at=dto.published_at,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            media=[ProductMediaResponse.from_dto(item) for item in dto.media],
            details=(
                ProductDetailResponse.from_dto(dto.details)
                if dto.details is not None
                else None
            ),
            colors=[ProductColorResponse.from_dto(item) for item in dto.colors],
            sizes=[ProductSizeResponse.from_dto(item) for item in dto.sizes],
            measurement_guide=(
                ProductMeasurementGuideResponse.from_dto(dto.measurement_guide)
                if dto.measurement_guide is not None
                else None
            ),
            customization=(
                ProductCustomizationResponse.from_dto(dto.customization)
                if dto.customization is not None
                else None
            ),
        )

    @classmethod
    def from_query_dto(
        cls,
        dto: ProductDetailQueryDTO,
    ) -> Self:
        return cls(
            id=dto.id,
            brand_id=dto.brand_id,
            collection_id=dto.collection_id,
            category_id=dto.category_id,
            product_code=dto.product_code,
            name=dto.name,
            slug=dto.slug,
            description=dto.description,
            status=dto.status,
            published_at=dto.published_at,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            media=[
                ProductMediaResponse(
                    id=item.id,
                    media_asset_id=item.media_asset_id,
                    alt_text=item.alt_text,
                    url=item.url,
                    mime_type=item.mime_type,
                    width=item.width,
                    height=item.height,
                    sort_order=item.sort_order,
                    is_primary=item.is_primary,
                )
                for item in dto.media
            ],
            details=(
                ProductDetailResponse.from_dto(dto.details)
                if dto.details is not None
                else None
            ),
            colors=[ProductColorResponse.from_dto(item) for item in dto.colors],
            sizes=[ProductSizeResponse.from_dto(item) for item in dto.sizes],
            measurement_guide=(
                ProductMeasurementGuideResponse.from_dto(dto.measurement_guide)
                if dto.measurement_guide is not None
                else None
            ),
            customization=(
                ProductCustomizationResponse.from_dto(dto.customization)
                if dto.customization is not None
                else None
            ),
        )


class ProductListImageResponse(BaseModel):
    id: UUID
    url: str
    mime_type: str | None
    width: int | None
    height: int | None


class ProductListItemResponse(BaseModel):
    id: UUID
    product_code: str
    name: str
    slug: str
    status: RecordStatus
    description: str | None

    brand_id: UUID
    collection_id: UUID
    category_id: UUID

    image: ProductListImageResponse | None

    created_at: datetime
    updated_at: datetime


class PaginationResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class ProductListResponse(BaseModel):
    items: list[ProductListItemResponse]
    pagination: PaginationResponse

    @classmethod
    def from_dto(
        cls,
        dto: ProductListResultDTO,
    ) -> Self:
        return cls(
            items=[
                ProductListItemResponse(
                    id=item.id,
                    product_code=item.product_code,
                    name=item.name,
                    slug=item.slug,
                    description=item.description,
                    status=item.status,
                    brand_id=item.brand_id,
                    collection_id=item.collection_id,
                    category_id=item.category_id,
                    image=(
                        ProductListImageResponse(
                            id=item.image.id,
                            url=item.image.url,
                            mime_type=item.image.mime_type,
                            width=item.image.width,
                            height=item.image.height,
                        )
                        if item.image is not None
                        else None
                    ),
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                )
                for item in dto.items
            ],
            pagination=PaginationResponse(
                page=dto.page,
                page_size=dto.page_size,
                total=dto.total,
                total_pages=dto.total_pages,
            ),
        )


class ProductSortField(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
    PRODUCT_CODE = "product_code"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class ProductQueryParams(BaseModel):
    search: str | None = None

    status: RecordStatus | None = None

    brand_id: UUID | None = None
    collection_id: UUID | None = None
    category_id: UUID | None = None

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    sort_by: ProductSortField = ProductSortField.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC


class ProductDetailQueryResponse(BaseModel):
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

    media: list[ProductMediaQueryResponse]
    details: ProductDetailResponse | None
    colors: list[ProductColorResponse]
    sizes: list[ProductSizeResponse]
    measurement_guide: ProductMeasurementGuideResponse | None
    customization: ProductCustomizationResponse | None

    @classmethod
    def from_dto(
        cls,
        dto: ProductDetailQueryDTO,
    ) -> Self:
        return cls(
            id=dto.id,
            brand_id=dto.brand_id,
            collection_id=dto.collection_id,
            category_id=dto.category_id,
            product_code=dto.product_code,
            name=dto.name,
            slug=dto.slug,
            description=dto.description,
            status=dto.status,
            published_at=dto.published_at,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            media=[ProductMediaQueryResponse.from_dto(item) for item in dto.media],
            details=(
                ProductDetailResponse.from_dto(dto.details)
                if dto.details is not None
                else None
            ),
            colors=[ProductColorResponse.from_dto(item) for item in dto.colors],
            sizes=[ProductSizeResponse.from_dto(item) for item in dto.sizes],
            measurement_guide=(
                ProductMeasurementGuideResponse.from_dto(dto.measurement_guide)
                if dto.measurement_guide is not None
                else None
            ),
            customization=(
                ProductCustomizationResponse.from_dto(dto.customization)
                if dto.customization is not None
                else None
            ),
        )


class UpdateProductRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = None

    brand_id: UUID | None = None
    collection_id: UUID | None = None
    category_id: UUID | None = None

    status: RecordStatus | None = None

    media: list[UpdateProductMediaRequest] | None = None
    details: UpdateProductDetailRequest | None = None
    colors: list[UpdateProductColorRequest] | None = None
    sizes: list[UpdateProductSizeRequest] | None = None
    measurement_guide: UpdateProductMeasurementGuideRequest | None = None
    customization: UpdateProductCustomizationRequest | None = None


# PublicsPublicFeaturedProductDTO
class PublicProductImageResponse(BaseModel):
    id: UUID
    url: str


class PublicFeaturedProductResponse(BaseModel):
    id: UUID
    product_code: str
    name: str
    slug: str
    description: str | None
    image: PublicProductImageResponse | None

    @classmethod
    def from_dto(
        cls,
        dto: PublicFeaturedProductDTO,
    ) -> "PublicFeaturedProductResponse":
        return cls(
            id=dto.id,
            product_code=dto.product_code,
            name=dto.name,
            slug=dto.slug,
            description=dto.description,
            image=(
                PublicProductImageResponse(
                    id=dto.image_id,
                    url=dto.image_url,
                )
                if dto.image_id is not None and dto.image_url is not None
                else None
            ),
        )


class PublicFeaturedProductListResponse(BaseModel):
    items: list[PublicFeaturedProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class PublicProductResponse(BaseModel):
    id: UUID
    product_code: str
    name: str
    slug: str
    description: str | None
    media: list[PublicProductImageResponse]

    @classmethod
    def from_dto(
        cls,
        dto: PublicProductDTO,
    ) -> "PublicProductResponse":
        return cls(
            id=dto.id,
            product_code=dto.product_code,
            name=dto.name,
            slug=dto.slug,
            description=dto.description,
            media=[
                PublicProductImageResponse(
                    id=media.id,
                    url=media.url,
                )
                for media in dto.media
            ],
        )


class PublicProductListResponse(BaseModel):
    items: list[PublicProductResponse]
    next_cursor: str | None
    has_more: bool


class PublicProductQuery(BaseModel):
    cursor: str | None = None

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )

    search: str | None = Field(
        default=None,
        max_length=100,
    )

    brand_id: UUID | None = None

    collection_id: UUID | None = None

    category_id: UUID | None = None

    sort_by: ProductSortBy = ProductSortBy.CREATED_AT

    sort_order: ProductSortOrder = ProductSortOrder.DESC

    @field_validator("search")
    @classmethod
    def validate_search(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        return value or None

    @field_validator("cursor")
    @classmethod
    def validate_cursor(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        return value or None

    def to_dto(self) -> PublicProductQueryDTO:
        return PublicProductQueryDTO(
            cursor=self.cursor,
            page_size=self.page_size,
            search=self.search,
            brand_id=self.brand_id,
            collection_id=self.collection_id,
            category_id=self.category_id,
            sort_by=self.sort_by,
            sort_order=self.sort_order,
        )
