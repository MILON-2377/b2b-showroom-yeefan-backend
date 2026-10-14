from uuid import UUID

from app.core.contracts.services.category import AbstractCategoryService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.categories.model import Category
from app.modules.media.exceptions import (
    MediaAssetNotFoundError,
    MediaAssetNotReadyError,
)
from app.modules.media.model import MediaAssetStatus
from app.modules.media.service import MediaUploadService
from app.shared.utils.slug_generator import slug_generator

from .dtos import (
    CategoryDTO,
    CategoryImageDTO,
    CategoryListItem,
    CreateCategoryDTO,
    PublicCategoryDTO,
    PublicCategoryListDTO,
    UpdateCategoryDTO,
)
from .exceptions import (
    CategoryNotFoundError,
    CategorySlugAlreadyExistsError,
)
from .query import CategoryListQuery, CategoryListResult


class CategoryService(AbstractCategoryService):
    def __init__(
        self, uow: AbstractUnitOfWork, media_upload_service: MediaUploadService
    ):
        self.uow = uow
        self.media_upload_service = media_upload_service

    async def create(
        self,
        *,
        payload: CreateCategoryDTO,
    ) -> CategoryListItem:
        slug = slug_generator(value=payload.name)

        if await self.uow.categories.exists_by_slug(slug):
            raise CategorySlugAlreadyExistsError(slug)

        image = None

        if payload.image_media_id is not None:
            media_asset = await self.uow.media_assets.get_by_id(payload.image_media_id)

            if media_asset is None:
                raise MediaAssetNotFoundError(payload.image_media_id)

            if media_asset.status != MediaAssetStatus.READY:
                raise MediaAssetNotReadyError(payload.image_media_id)

            image = CategoryImageDTO(
                id=media_asset.id,
                url=self.media_upload_service.get_asset_url(
                    media_asset=media_asset,
                ),
                mime_type=media_asset.mime_type,
                width=media_asset.width,
                height=media_asset.height,
            )

        category = Category(
            name=payload.name,
            slug=slug,
            description=payload.description,
            status=payload.status,
            image_media_id=payload.image_media_id,
        )

        await self.uow.categories.create(category)

        await self.uow.flush()

        await self.uow.commit()

        return CategoryListItem(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            status=category.status,
            image=image,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )

    async def get_by_id(
        self,
        category_id: UUID,
    ) -> CategoryListItem:
        category = await self.uow.categories.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(category_id)

        image = None

        if category.image_media is not None:
            image = CategoryImageDTO(
                id=category.image_media.id,
                url=self.media_upload_service.get_asset_url(
                    media_asset=category.image_media,
                ),
                mime_type=category.image_media.mime_type,
                width=category.image_media.width,
                height=category.image_media.height,
            )

        return CategoryListItem(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            status=category.status,
            image=image,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )

    async def get_by_slug(
        self,
        slug: str,
    ) -> Category:
        category = await self.uow.categories.get_by_slug(slug)

        if category is None:
            raise CategoryNotFoundError(slug)

        return category

    async def list(
        self,
        *,
        search: str | None = None,
        status: RecordStatus | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> CategoryListResult:
        query = CategoryListQuery(
            search=search,
            status=status,
            page=page,
            page_size=page_size,
        )

        result = await self.uow.categories.list(query=query)

        items: list[CategoryListItem] = []

        for category in result.items:
            image = None

            if category.image_media is not None:
                image = CategoryImageDTO(
                    id=category.image_media.id,
                    url=self.media_upload_service.get_asset_url(
                        media_asset=category.image_media,
                    ),
                    mime_type=category.image_media.mime_type,
                    width=category.image_media.width,
                    height=category.image_media.height,
                )

            items.append(
                CategoryListItem(
                    id=category.id,
                    name=category.name,
                    slug=category.slug,
                    description=category.description,
                    status=category.status,
                    image=image,
                    created_at=category.created_at,
                    updated_at=category.updated_at,
                )
            )

        return CategoryListResult(
            items=items,
            total=result.total,
        )

    async def delete(
        self,
        category_id: UUID,
    ) -> None:
        category = await self.uow.categories.get_by_id(category_id)

        if category is None:
            raise ValueError(f"Category '{category_id}' not found")

        await self.uow.categories.delete(category)
        await self.uow.commit()

    async def update(
        self,
        *,
        category_id: UUID,
        payload: UpdateCategoryDTO,
    ) -> CategoryListItem:
        category = await self.uow.categories.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(category_id)

        if payload.name is not None and payload.name != category.name:
            category.name = payload.name
            category.slug = slug_generator(payload.name)

        if payload.description is not None:
            category.description = payload.description

        if payload.status is not None:
            category.status = payload.status

        if payload.image_media_id is not None:
            media_asset = await self.uow.media_assets.get_by_id(payload.image_media_id)

            if media_asset is None:
                raise MediaAssetNotFoundError(payload.image_media_id)

            if media_asset.status != MediaAssetStatus.READY:
                raise MediaAssetNotReadyError(payload.image_media_id)

            old_media_asset = category.image_media

            category.image_media_id = payload.image_media_id

            if (
                old_media_asset is not None
                and old_media_asset.id != payload.image_media_id
            ):
                await self.media_upload_service.mark_for_deletion(
                    media_asset=old_media_asset,
                )

        await self.uow.categories.update(category)
        await self.uow.flush()
        await self.uow.commit()

        image = None

        if category.image_media is not None:
            image = CategoryImageDTO(
                id=category.image_media.id,
                url=self.media_upload_service.get_asset_url(
                    media_asset=category.image_media,
                ),
                mime_type=category.image_media.mime_type,
                width=category.image_media.width,
                height=category.image_media.height,
            )

        return CategoryListItem(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            status=category.status,
            image=image,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )

    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
    ) -> PublicCategoryListDTO:
        result = await self.uow.categories.list_public(
            page=page,
            page_size=page_size,
        )

        return PublicCategoryListDTO(
            items=tuple(
                PublicCategoryDTO(
                    id=category.id,
                    name=category.name,
                    slug=category.slug,
                    status=category.status,
                    image_id=(
                        category.image_media.id
                        if category.image_media is not None
                        else None
                    ),
                    image_url=(
                        category.image_media.secure_url
                        if category.image_media is not None
                        else None
                    ),
                )
                for category in result.items
            ),
            total=result.total,
        )

    # Validation
    async def validate_for_product(
        self,
        *,
        category_id: UUID,
    ) -> CategoryDTO:
        category = await self.uow.categories.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(category_id)

        return self._to_dto(category)

    @staticmethod
    def _to_dto(category: Category) -> CategoryDTO:
        return CategoryDTO(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            image_media_id=category.image_media_id,
            status=category.status,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
