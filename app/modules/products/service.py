from __future__ import annotations

import math
from datetime import datetime, timezone
from uuid import UUID

from app.core.contracts.services.brand import AbstractBrandService
from app.core.contracts.services.category import AbstractCategoryService
from app.core.contracts.services.collection import AbstractCollectionService
from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.services.product import AbstractProductService
from app.core.contracts.services.product_color import AbstractProductColorService
from app.core.contracts.services.product_customization import (
    AbstractProductCustomizationService,
)
from app.core.contracts.services.product_detail import AbstractProductDetailService
from app.core.contracts.services.product_measurement_guide import (
    AbstractProductMeasurementGuideService,
)
from app.core.contracts.services.product_media import AbstractProductMediaService
from app.core.contracts.services.product_size import AbstractProductSizeService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.media.model import MediaAssetStatus
from app.modules.product_colors.dtos import CreateProductColorDTO, UpdateProductColorDTO
from app.modules.product_colors.service import ProductColorService
from app.modules.product_customizations.dtos.product_customization import (
    CreateProductCustomizationDTO,
    UpdateProductCustomizationDTO,
)
from app.modules.product_customizations.dtos.product_customization_option import (
    CreateProductCustomizationOptionDTO,
)
from app.modules.product_customizations.exceptions import (
    ProductCustomizationCannotBeNullError,
)
from app.modules.product_customizations.services.product_customization import (
    ProductCustomizationService,
)
from app.modules.product_details.dtos import (
    CreateProductDetailDTO,
    UpdateProductDetailDTO,
)
from app.modules.product_details.exceptions import ProductDetailsCannotBeNullError
from app.modules.product_details.service import ProductDetailService
from app.modules.product_media.dtos import (
    CreateProductMediaDTO,
    ProductMediaQueryDTO,
    UpdateProductMediaDTO,
)
from app.modules.product_media.exceptions import ProductMediaCannotBeNullError
from app.modules.product_media.model import ProductMedia
from app.modules.product_sizes.dtos.product_measurement_guide import (
    CreateProductMeasurementGuideDTO,
    UpdateProductMeasurementGuideDTO,
)
from app.modules.product_sizes.dtos.product_size import (
    CreateProductSizeDTO,
    CreateProductSizeWithMeasurementDTO,
    UpdateProductSizeDTO,
)
from app.modules.product_sizes.dtos.size_measurement import CreateSizeMeasurementDTO
from app.modules.product_sizes.exceptions import (
    ProductMeasurementGuideCannotBeNullError,
)
from app.modules.product_sizes.services.product_measurement_guide import (
    ProductMeasurementGuideService,
)
from app.modules.product_sizes.services.product_size import ProductSizeService
from app.modules.products.dtos import (
    UNSET,
    CreateProductDTO,
    ProductDetailQueryDTO,
    ProductDTO,
    ProductListImageDTO,
    ProductListItem,
    ProductListResultDTO,
    ProductQueryDTO,
    PublicFeaturedProductDTO,
    PublicFeaturedProductListDTO,
    PublicProductDTO,
    PublicProductListResult,
    PublicProductMediaDTO,
    PublicProductQueryDTO,
    UpdateProductDTO,
)
from app.modules.products.exceptions import (
    ProductCodeAlreadyExistsError,
    ProductNotFoundError,
    ProductSlugAlreadyExistsError,
)
from app.modules.products.model import Product
from app.modules.products.schemas import CreateProductRequest, UpdateProductRequest
from app.shared.utils.create_product_code import create_product_code
from app.shared.utils.slug import create_slug


class ProductService(AbstractProductService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        brand_service: AbstractBrandService,
        collection_service: AbstractCollectionService,
        category_service: AbstractCategoryService,
        product_media_service: AbstractProductMediaService,
        product_detail_service: AbstractProductDetailService,
        product_color_service: AbstractProductColorService,
        product_size_service: AbstractProductSizeService,
        product_measurement_guide_service: AbstractProductMeasurementGuideService,
        product_customization_service: AbstractProductCustomizationService,
        media_upload_service: AbstractMediaUploadService,
    ):
        self.uow = uow
        self.brand_service = brand_service
        self.collection_service = collection_service
        self.category_service = category_service
        self.product_media_service = product_media_service
        self.product_detail_service = product_detail_service
        self.product_color_service = product_color_service
        self.product_size_service = product_size_service
        self.product_measurement_guide_service = product_measurement_guide_service
        self.product_customization_service = product_customization_service
        self.media_upload_service = media_upload_service

    async def create(self, *, payload: CreateProductDTO) -> ProductDTO:

        collection = await self.collection_service.validate_for_product(
            collection_id=payload.collection_id
        )

        await self.category_service.validate_for_product(
            category_id=payload.category_id,
        )

        base_slug = create_slug(payload.name)
        slug = await self.generate_unique_slug(
            brand_id=collection.brand_id, base_slug=base_slug
        )
        product_code = create_product_code(payload.name)

        await self.validate_product_code(
            brand_id=collection.brand_id,
            product_code=product_code,
        )

        await self.validate_slug(
            brand_id=collection.brand_id,
            slug=slug,
        )

        # Product Transaction
        product = Product(
            brand_id=collection.brand_id,
            collection_id=payload.collection_id,
            category_id=payload.category_id,
            product_code=product_code,
            name=payload.name,
            slug=slug,
            description=payload.description,
        )

        await self.uow.products.create(product)
        await self.uow.flush()

        # Product Media Transaction
        media = await self.product_media_service.create_many(
            product_id=product.id, payloads=payload.media
        )

        # Product Detail
        details = None

        if payload.details is not None:
            details = await self.product_detail_service.create(
                product_id=product.id,
                payload=payload.details,
            )

        # Product Color
        colors = await self.product_color_service.create_many(
            product_id=product.id, payloads=payload.colors
        )

        # Product Size
        sizes = await self.product_size_service.create_many(
            product_id=product.id, payloads=payload.sizes
        )

        # Product Measurement Guide
        measurement_guide = None

        if payload.measurement_guide is not None:
            measurement_guide = await self.product_measurement_guide_service.create(
                product_id=product.id,
                payload=payload.measurement_guide,
            )

        # Product Customization
        customization = None

        if payload.customization is not None:
            customization = await self.product_customization_service.create(
                product_id=product.id,
                payload=payload.customization,
            )

        await self.uow.commit()

        return ProductDTO(
            id=product.id,
            brand_id=product.brand_id,
            collection_id=product.collection_id,
            category_id=product.category_id,
            product_code=product.product_code,
            name=product.name,
            slug=product.slug,
            description=product.description,
            status=product.status,
            published_at=product.published_at,
            created_at=product.created_at,
            updated_at=product.updated_at,
            media=tuple(media),
            details=details,
            colors=tuple(colors),
            sizes=tuple(sizes),
            measurement_guide=measurement_guide,
            customization=customization,
        )

    async def list(self, *, query: ProductQueryDTO) -> ProductListResultDTO:

        result = await self.uow.products.list(query=query)

        items = [self._to_list_item(product) for product in result.items]

        total_pages = (
            math.ceil(result.total / query.page_size) if result.total > 0 else 0
        )

        return ProductListResultDTO(
            items=items,
            total=result.total,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages,
        )

    async def list_featured(
        self,
        *,
        page: int,
        page_size: int,
    ) -> PublicFeaturedProductListDTO:
        result = await self.uow.products.list_featured(
            page=page,
            page_size=page_size,
        )

        return PublicFeaturedProductListDTO(
            items=tuple(
                self._to_public_featured_dto(product) for product in result.items
            ),
            total=result.total,
        )

    async def list_public(
        self,
        *,
        query: PublicProductQueryDTO,
    ) -> PublicProductListResult:
        result = await self.uow.products.list_public(
            query=query,
        )

        return PublicProductListResult(
            items=tuple(self._to_public_dto(product) for product in result.items),
            next_cursor=result.next_cursor,
            has_more=result.has_more,
        )

    async def get_by_id(
        self,
        product_id: UUID,
    ) -> ProductDetailQueryDTO:

        product = await self.uow.products.get_by_id(
            product_id,
        )

        if product is None:
            raise ProductNotFoundError(product_id)

        return self._to_detail_query_dto(product)

    async def get_public_by_id(
        self,
        product_id: UUID,
    ) -> ProductDetailQueryDTO:

        product = await self.uow.products.get_public_by_id(
            product_id,
        )

        if product is None:
            raise ProductNotFoundError(product_id)

        return self._to_detail_query_dto(product)

    async def update(
        self,
        *,
        product_id: UUID,
        payload: UpdateProductDTO,
    ) -> ProductDTO:
        product = await self.uow.products.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError(product_id)

        if payload.name is not UNSET:
            product.name = payload.name

        if payload.description is not UNSET:
            product.description = payload.description

        if payload.collection_id is not UNSET:
            product.collection_id = payload.collection_id

        if payload.category_id is not UNSET:
            product.category_id = payload.category_id

        if payload.status is not UNSET:
            product.status = payload.status

            if payload.status == RecordStatus.PUBLISHED:
                if product.published_at is None:
                    product.published_at = datetime.now(timezone.utc)
            else:
                product.published_at = None

        if payload.media is not UNSET:
            if payload.media is None:
                raise ProductMediaCannotBeNullError()

            await self.product_media_service.update_many(
                product_id=product_id,
                payloads=payload.media,
            )

        if payload.details is not UNSET:
            if payload.details is None:
                raise ProductDetailsCannotBeNullError()

            await self.product_detail_service.update(
                product_id=product_id,
                payload=payload.details,
            )

        if payload.colors is not UNSET:
            await self.product_color_service.update_many(
                product_id=product_id,
                payloads=payload.colors,
            )

        if payload.sizes is not UNSET:
            await self.product_size_service.update_many(
                product_id=product_id,
                payloads=payload.sizes,
            )

        if payload.measurement_guide is not UNSET:
            if payload.measurement_guide is None:
                raise ProductMeasurementGuideCannotBeNullError()

            await self.product_measurement_guide_service.update(
                product_id=product_id,
                payload=payload.measurement_guide,
            )

        if payload.customization is not UNSET:
            if payload.customization is None:
                raise ProductCustomizationCannotBeNullError()

            await self.product_customization_service.update(
                product_id=product_id,
                payload=payload.customization,
            )

        await self.uow.flush()

        await self.uow.commit()

        return await self.get_by_id(product_id)

    # Validation
    async def validate_product_code(
        self,
        *,
        brand_id: UUID,
        product_code: str,
    ) -> None:
        exists = await self.uow.products.exists_by_product_code(
            brand_id,
            product_code,
        )

        if exists:
            raise ProductCodeAlreadyExistsError(product_code)

    async def validate_slug(
        self,
        *,
        brand_id: UUID,
        slug: str,
        exclude_id: UUID | None = None,
    ) -> None:
        exists = await self.uow.products.exists_by_slug(
            brand_id,
            slug,
            exclude_id=exclude_id,
        )

        if exists:
            raise ProductSlugAlreadyExistsError(slug)

    # Static Method
    @staticmethod
    def _to_create_product_dto(
        payload: CreateProductRequest,
    ) -> CreateProductDTO:
        return CreateProductDTO(
            collection_id=payload.collection_id,
            category_id=payload.category_id,
            name=payload.name,
            description=payload.description,
            media=tuple(
                CreateProductMediaDTO(
                    media_asset_id=item.media_asset_id,
                    alt_text=item.alt_text,
                    sort_order=item.sort_order,
                    is_primary=item.is_primary,
                )
                for item in payload.media
            ),
            details=(
                CreateProductDetailDTO(
                    garment_type=payload.details.garment_type,
                    silhouette=payload.details.silhouette,
                    length=payload.details.length,
                    fabric=payload.details.fabric,
                    secondary_fabric=payload.details.secondary_fabric,
                    lining=payload.details.lining,
                    neckline=payload.details.neckline,
                    back_style=payload.details.back_style,
                    waistline=payload.details.waistline,
                    sleeve_type=payload.details.sleeve_type,
                    sleeve_length=payload.details.sleeve_length,
                    train=payload.details.train,
                    embellishment=payload.details.embellishment,
                    closure=payload.details.closure,
                    internal_support=payload.details.internal_support,
                )
                if payload.details is not None
                else None
            ),
            colors=tuple(
                CreateProductColorDTO(
                    name=item.name,
                    sort_order=item.sort_order,
                )
                for item in payload.colors
            ),
            sizes=tuple(
                CreateProductSizeWithMeasurementDTO(
                    size=CreateProductSizeDTO(
                        name=item.name,
                        sort_order=item.sort_order,
                    ),
                    measurement=(
                        CreateSizeMeasurementDTO(
                            bust=item.measurement.bust,
                            waist=item.measurement.waist,
                            hips=item.measurement.hips,
                            hollow_to_hem=item.measurement.hollow_to_hem,
                            unit=item.measurement.unit,
                        )
                        if item.measurement is not None
                        else None
                    ),
                )
                for item in payload.sizes
            ),
            measurement_guide=(
                CreateProductMeasurementGuideDTO(
                    title=payload.measurement_guide.title,
                    description=payload.measurement_guide.description,
                    measurement_unit=payload.measurement_guide.measurement_unit,
                    notes=payload.measurement_guide.notes,
                )
                if payload.measurement_guide is not None
                else None
            ),
            customization=(
                CreateProductCustomizationDTO(
                    is_customizable=payload.customization.is_customizable,
                    notes=payload.customization.notes,
                    options=tuple(
                        CreateProductCustomizationOptionDTO(
                            option_type=option.option_type,
                            details=option.details,
                            sort_order=option.sort_order,
                        )
                        for option in payload.customization.options
                    ),
                )
                if payload.customization is not None
                else None
            ),
        )

    async def generate_unique_slug(
        self,
        *,
        brand_id: UUID,
        base_slug: str,
    ) -> str:
        slug = base_slug
        counter = 2

        while await self.uow.products.exists_by_slug(
            brand_id,
            slug,
        ):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def _to_list_item(
        self,
        product: Product,
    ) -> ProductListItem:

        image = self._get_primary_image(
            product.media,
        )

        return ProductListItem(
            id=product.id,
            product_code=product.product_code,
            name=product.name,
            slug=product.slug,
            description=product.description,
            status=product.status,
            brand_id=product.brand_id,
            collection_id=product.collection_id,
            category_id=product.category_id,
            image=image,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    def _get_primary_image(
        self,
        media: list[ProductMedia],
    ) -> ProductListImageDTO | None:

        if not media:
            return None

        primary = next(
            (item for item in media if item.is_primary),
            None,
        )

        if primary is None:
            primary = min(
                media,
                key=lambda item: item.sort_order,
            )

        asset = primary.media_asset

        return ProductListImageDTO(
            id=asset.id,
            url=self.media_upload_service.get_asset_url(
                media_asset=asset,
            ),
            mime_type=asset.mime_type,
            width=asset.width,
            height=asset.height,
        )

    def _to_detail_query_dto(
        self,
        product: Product,
    ) -> ProductDetailQueryDTO:
        return ProductDetailQueryDTO(
            id=product.id,
            brand_id=product.brand_id,
            collection_id=product.collection_id,
            category_id=product.category_id,
            product_code=product.product_code,
            name=product.name,
            slug=product.slug,
            description=product.description,
            status=product.status,
            published_at=product.published_at,
            created_at=product.created_at,
            updated_at=product.updated_at,
            media=[self._to_media_query_dto(item) for item in product.media],
            details=(
                ProductDetailService._to_dto(product.details)
                if product.details
                else None
            ),
            colors=[ProductColorService._to_dto(item) for item in product.colors],
            sizes=[ProductSizeService._to_dto(item) for item in product.sizes],
            measurement_guide=(
                ProductMeasurementGuideService._to_dto(product.measurement_guide)
                if product.measurement_guide
                else None
            ),
            customization=(
                ProductCustomizationService._to_dto(product.customization)
                if product.customization
                else None
            ),
        )

    def _to_detail_dto(
        self,
        product: Product,
    ) -> ProductDetailQueryDTO:

        return ProductDetailQueryDTO(
            id=product.id,
            brand_id=product.brand_id,
            collection_id=product.collection_id,
            category_id=product.category_id,
            product_code=product.product_code,
            name=product.name,
            slug=product.slug,
            description=product.description,
            status=product.status,
            published_at=product.published_at,
            created_at=product.created_at,
            updated_at=product.updated_at,
            media=[self._to_media_query_dto(item) for item in product.media],
            details=(
                self.product_detail_service._to_dto(product.details)
                if product.details is not None
                else None
            ),
            colors=[
                self.product_color_service._to_dto(item) for item in product.colors
            ],
            sizes=[self.product_size_service._to_dto(item) for item in product.sizes],
            measurement_guide=(
                self.product_measurement_guide_service._to_dto(
                    product.measurement_guide
                )
                if product.measurement_guide is not None
                else None
            ),
            customization=(
                self.product_customization_service._to_dto(product.customization)
                if product.customization is not None
                else None
            ),
        )

    def _to_media_query_dto(
        self,
        product_media: ProductMedia,
    ) -> ProductMediaQueryDTO:
        asset = product_media.media_asset

        return ProductMediaQueryDTO(
            id=product_media.id,
            media_asset_id=asset.id,
            alt_text=product_media.alt_text,
            url=self.media_upload_service.get_asset_url(
                media_asset=asset,
            ),
            mime_type=asset.mime_type,
            width=asset.width,
            height=asset.height,
            sort_order=product_media.sort_order,
            is_primary=product_media.is_primary,
        )

    @staticmethod
    def _to_update_product_dto(
        payload: UpdateProductRequest,
    ) -> UpdateProductDTO:
        return UpdateProductDTO(
            name=payload.name,
            description=payload.description,
            collection_id=payload.collection_id,
            category_id=payload.category_id,
            status=payload.status,
            media=(
                tuple(
                    UpdateProductMediaDTO(
                        id=item.id,
                        media_asset_id=item.media_asset_id,
                        alt_text=item.alt_text,
                        sort_order=item.sort_order,
                        is_primary=item.is_primary,
                    )
                    for item in payload.media
                )
                if payload.media is not None
                else UNSET
            ),
            details=(
                UpdateProductDetailDTO(
                    garment_type=payload.details.garment_type,
                    silhouette=payload.details.silhouette,
                    length=payload.details.length,
                    fabric=payload.details.fabric,
                    secondary_fabric=payload.details.secondary_fabric,
                    lining=payload.details.lining,
                    neckline=payload.details.neckline,
                    back_style=payload.details.back_style,
                    waistline=payload.details.waistline,
                    sleeve_type=payload.details.sleeve_type,
                    sleeve_length=payload.details.sleeve_length,
                    train=payload.details.train,
                    embellishment=payload.details.embellishment,
                    closure=payload.details.closure,
                    internal_support=payload.details.internal_support,
                )
                if payload.details is not None
                else UNSET
            ),
            colors=(
                tuple(
                    UpdateProductColorDTO(
                        id=item.id,
                        name=item.name,
                        sort_order=item.sort_order,
                    )
                    for item in payload.colors
                )
                if payload.colors is not None
                else UNSET
            ),
            sizes=(
                tuple(
                    UpdateProductSizeDTO(
                        id=item.id,
                        name=item.name,
                        sort_order=item.sort_order,
                    )
                    for item in payload.sizes
                )
                if payload.sizes is not None
                else UNSET
            ),
            measurement_guide=(
                UpdateProductMeasurementGuideDTO(
                    title=payload.measurement_guide.title,
                    description=payload.measurement_guide.description,
                    measurement_unit=payload.measurement_guide.measurement_unit,
                    notes=payload.measurement_guide.notes,
                )
                if payload.measurement_guide is not None
                else UNSET
            ),
            customization=(
                UpdateProductCustomizationDTO(
                    is_customizable=payload.customization.is_customizable,
                    notes=payload.customization.notes,
                )
                if payload.customization is not None
                else UNSET
            ),
        )

    @staticmethod
    def _to_public_featured_dto(
        product: Product,
    ) -> PublicFeaturedProductDTO:
        primary_media = next(
            (
                media
                for media in product.media
                if media.is_primary and media.media_asset is not None
            ),
            None,
        )

        return PublicFeaturedProductDTO(
            id=product.id,
            product_code=product.product_code,
            name=product.name,
            slug=product.slug,
            description=product.description,
            image_id=(
                primary_media.media_asset.id if primary_media is not None else None
            ),
            image_url=(
                primary_media.media_asset.secure_url
                if primary_media is not None
                else None
            ),
        )

    @staticmethod
    def _to_public_dto(
        product: Product,
    ) -> PublicProductDTO:
        product_media = sorted(
            product.media,
            key=lambda media: (
                not media.is_primary,
                media.sort_order,
                media.created_at,
            ),
        )

        media = []

        for product_media_item in product_media:
            media_asset = product_media_item.media_asset

            if media_asset is None:
                continue

            if media_asset.status != MediaAssetStatus.READY:
                continue

            if not media_asset.secure_url:
                continue

            media.append(
                PublicProductMediaDTO(
                    id=media_asset.id,
                    url=media_asset.secure_url,
                )
            )

        return PublicProductDTO(
            id=product.id,
            product_code=product.product_code,
            name=product.name,
            slug=product.slug,
            description=product.description,
            media=tuple(media),
        )
