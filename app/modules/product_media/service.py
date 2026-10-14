from uuid import UUID

from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.services.product_media import (
    AbstractProductMediaService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.media.exceptions import (
    MediaAssetNotFoundError,
    MediaAssetNotReadyError,
)
from app.modules.media.model import MediaAssetStatus
from app.modules.product_media.dtos import (
    CreateProductMediaDTO,
    ProductMediaDTO,
    UpdateProductMediaDTO,
)
from app.modules.product_media.exceptions import (
    DuplicateProductMediaError,
    MultiplePrimaryProductMediaError,
    ProductMediaNotFoundError,
)
from app.modules.product_media.model import ProductMedia


class ProductMediaService(AbstractProductMediaService):
    def __init__(
        self, uow: AbstractUnitOfWork, upload_media_service: AbstractMediaUploadService
    ) -> None:
        self.uow = uow
        self.upload_media_service = upload_media_service

    async def create_many(
        self,
        *,
        product_id: UUID,
        payloads: list[CreateProductMediaDTO],
    ) -> list[ProductMediaDTO]:

        if not payloads:
            return []

        await self._validate_media_assets(payloads)

        product_media = [
            ProductMedia(
                product_id=product_id,
                media_asset_id=payload.media_asset_id,
                alt_text=payload.alt_text,
                sort_order=payload.sort_order,
                is_primary=payload.is_primary,
            )
            for payload in payloads
        ]

        product_media = await self.uow.product_media.create_many(product_media)

        return [self._to_dto(item) for item in product_media]

    async def create(
        self,
        *,
        product_id: UUID,
        media_asset_id: UUID,
        alt_text: str | None = None,
        sort_order: int = 0,
        is_primary: bool = False,
    ) -> ProductMediaDTO:
        product_media = ProductMedia(
            product_id=product_id,
            media_asset_id=media_asset_id,
            alt_text=alt_text,
            sort_order=sort_order,
            is_primary=is_primary,
        )

        product_media = await self.uow.product_media.create(product_media)

        return self._to_dto(product_media)

    async def get_by_id(
        self,
        product_media_id: UUID,
    ) -> ProductMediaDTO:
        product_media = await self.uow.product_media.get_by_id(product_media_id)

        if product_media is None:
            raise ProductMediaNotFoundError(product_media_id)

        return self._to_dto(product_media)

    async def list_by_product(
        self,
        product_id: UUID,
    ) -> list[ProductMediaDTO]:
        product_media = await self.uow.product_media.get_by_product_id(product_id)

        return [self._to_dto(media) for media in product_media]

    async def update(
        self,
        product_media_id: UUID,
        *,
        alt_text: str | None,
        sort_order: int,
        is_primary: bool,
    ) -> ProductMediaDTO:
        product_media = await self.uow.product_media.get_by_id(product_media_id)

        if product_media is None:
            raise ProductMediaNotFoundError(product_media_id)

        product_media.alt_text = alt_text
        product_media.sort_order = sort_order
        product_media.is_primary = is_primary

        product_media = await self.uow.product_media.update(product_media)

        await self.uow.commit()
        await self.uow.refresh(product_media)

        return self._to_dto(product_media)

    async def update_many(
        self,
        *,
        product_id: UUID,
        payloads: tuple[UpdateProductMediaDTO, ...],
    ) -> list[ProductMediaDTO]:
        payloads_list = list(payloads)

        existing_media = await self.uow.product_media.get_by_product_id(
            product_id=product_id,
        )

        await self._validate_existing_media_ids(
            payloads=payloads_list,
            existing_media=existing_media,
        )

        await self._validate_media_assets(
            payloads=payloads_list,
        )

        self._validate_primary_media(payloads_list)

        existing_by_id = {item.id: item for item in existing_media}

        submitted_ids = {
            payload.id for payload in payloads_list if payload.id is not None
        }

        removed_media = [
            item for item in existing_media if item.id not in submitted_ids
        ]

        if removed_media:
            await self.media_asset_service.mark_for_deletion_many(
                media_asset_ids=[item.media_asset_id for item in removed_media],
            )

            await self.uow.product_media.delete_many(
                removed_media,
            )

        new_media: list[ProductMedia] = []
        updated_media: list[ProductMedia] = []
        old_media_asset_ids: list[UUID] = []

        for payload in payloads_list:
            if payload.id is None:
                new_media.append(
                    ProductMedia(
                        product_id=product_id,
                        media_asset_id=payload.media_asset_id,
                        alt_text=payload.alt_text,
                        sort_order=payload.sort_order,
                        is_primary=payload.is_primary,
                    )
                )
                continue

            product_media = existing_by_id[payload.id]

            if product_media.media_asset_id != payload.media_asset_id:
                old_media_asset_ids.append(product_media.media_asset_id)

            product_media.media_asset_id = payload.media_asset_id
            product_media.alt_text = payload.alt_text
            product_media.sort_order = payload.sort_order
            product_media.is_primary = payload.is_primary

            updated_media.append(product_media)

        if old_media_asset_ids:
            await self.media_asset_service.mark_for_deletion_many(
                media_asset_ids=old_media_asset_ids,
            )

        if new_media:
            await self.uow.product_media.create_many(
                new_media,
            )

        if updated_media:
            await self.uow.product_media.update_many(
                updated_media,
            )

        return [self._to_dto(item) for item in [*updated_media, *new_media]]

    async def delete(
        self,
        product_media_id: UUID,
    ) -> None:
        product_media = await self.uow.product_media.get_by_id(product_media_id)

        if product_media is None:
            raise ProductMediaNotFoundError(product_media_id)

        await self.uow.product_media.delete(product_media)

        await self.uow.commit()

    # Validation
    async def _validate_existing_media_ids(
        self,
        *,
        payloads: list[UpdateProductMediaDTO],
        existing_media: list[ProductMedia],
    ) -> None:
        existing_ids = {item.id for item in existing_media}

        for payload in payloads:
            if payload.id is None:
                continue

            if payload.id not in existing_ids:
                raise ProductMediaNotFoundError(payload.id)

    async def _validate_media_assets(
        self,
        payloads: list[CreateProductMediaDTO],
    ) -> None:
        media_asset_ids = [payload.media_asset_id for payload in payloads]

        seen_media_asset_ids: set[UUID] = set()

        for media_asset_id in media_asset_ids:
            if media_asset_id in seen_media_asset_ids:
                raise DuplicateProductMediaError(media_asset_id)

            seen_media_asset_ids.add(media_asset_id)

        media_assets = await self.uow.media_assets.get_by_ids(
            media_asset_ids=media_asset_ids
        )

        media_assets_by_id = {asset.id: asset for asset in media_assets}

        for media_asset_id in media_asset_ids:
            media_asset = media_assets_by_id.get(media_asset_id)

            if media_asset is None:
                raise MediaAssetNotFoundError(media_asset_id)

            if media_asset.status != MediaAssetStatus.READY:
                raise MediaAssetNotReadyError(media_asset_id)

    def _validate_primary_media(
        self,
        payloads: list[UpdateProductMediaDTO],
    ) -> None:
        primary_count = sum(1 for payload in payloads if payload.is_primary)

        if primary_count > 1:
            raise MultiplePrimaryProductMediaError()

    @staticmethod
    def _to_dto(
        product_media: ProductMedia,
    ) -> ProductMediaDTO:
        return ProductMediaDTO(
            id=product_media.id,
            product_id=product_media.product_id,
            media_asset_id=product_media.media_asset_id,
            alt_text=product_media.alt_text,
            sort_order=product_media.sort_order,
            is_primary=product_media.is_primary,
            created_at=product_media.created_at,
            updated_at=product_media.updated_at,
        )
