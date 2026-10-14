import math
from uuid import UUID

from app.core.contracts.services.brand import AbstractBrandService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.errors.base import (
    BrandHasCollectionsError,
    BrandNotFoundError,
    BrandSlugAlreadyExistsError,
)
from app.core.models import RecordStatus
from app.modules.brands.dtos import (
    BrandDTO,
    PublicBrandListDTO,
    PublicBrandQueryDTO,
)
from app.modules.brands.model import Brand
from app.modules.brands.query import BrandListQuery, BrandListResult
from app.shared.utils.slug import create_slug


class BrandService(AbstractBrandService):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def list_public(
        self,
        query: PublicBrandQueryDTO,
    ) -> PublicBrandListDTO:
        brands, total = await self.uow.brands.list_public(
            page=query.page,
            page_size=query.page_size,
            search=query.search,
        )

        items = [self._to_dto(brand) for brand in brands]

        return PublicBrandListDTO(
            items=items,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=math.ceil(total / query.page_size) if total else 0,
        )

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        logo_media_url: str | None = None,
        status: RecordStatus = RecordStatus.DRAFT,
    ) -> Brand:

        slug = create_slug(name)

        if await self.uow.brands.exists_by_slug(slug):
            raise ValueError(f"Brand slug '{slug}' already exists")

        brand = Brand(
            name=name,
            slug=slug,
            description=description,
            logo_media_url=logo_media_url,
            status=status,
        )

        await self.uow.brands.add(brand)
        await self.uow.commit()

        return brand

    async def get_by_id(self, brand_id: UUID) -> Brand | None:
        return await self.uow.brands.get_by_id(brand_id)

    async def get_by_slug(self, slug: str) -> Brand | None:
        return await self.uow.brands.get_by_slug(slug)

    async def list(self, query: BrandListQuery) -> BrandListResult:
        return await self.uow.brands.list(query)

    async def delete(self, brand_id: UUID) -> None:
        brand = await self.uow.brands.get_by_id(brand_id)

        if brand is None:
            raise BrandNotFoundError(brand_id)

        has_collections = await self.uow.collections.exists_by_brand_id(brand_id)

        if has_collections:
            raise BrandHasCollectionsError(brand_id)

        await self.uow.brands.delete(brand)

        await self.uow.commit()

    async def update(
        self,
        brand_id: UUID,
        name: str,
        description: str | None = None,
        status: RecordStatus | None = None,
    ) -> Brand:

        brand = await self.uow.brands.get_by_id(brand_id)

        if brand is None:
            raise BrandNotFoundError(brand_id)

        slug = create_slug(name)

        if slug != brand.slug:
            exists = await self.uow.brands.exists_by_slug(
                slug,
                exclude_id=brand_id,
            )

            if exists:
                raise BrandSlugAlreadyExistsError(slug)

        brand.name = name
        brand.slug = slug
        brand.description = description

        if status is not None:
            brand.status = status

        await self.uow.brands.update(brand)

        await self.uow.commit()

        await self.uow.refresh(brand)

        return brand

    # Validation
    async def validate_for_product(
        self,
        *,
        brand_id: UUID,
    ) -> BrandDTO:
        brand = await self.uow.brands.get_by_id(brand_id)

        if brand is None:
            raise BrandNotFoundError(brand_id)

        return self._to_dto(brand)

    @staticmethod
    def _to_dto(brand: Brand) -> BrandDTO:
        return BrandDTO(
            id=brand.id,
            name=brand.name,
            slug=brand.slug,
            description=brand.description,
            status=brand.status,
            created_at=brand.created_at,
            updated_at=brand.updated_at,
        )
