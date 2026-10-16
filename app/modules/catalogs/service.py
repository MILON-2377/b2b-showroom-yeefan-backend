import math
from uuid import UUID

from app.core.contracts.services.catalog import AbstractCatalogService
from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.catalogs.dtos import (
    AdminCatalogDTO,
    AdminCatalogListDTO,
    AdminCatalogQueryDTO,
    CatalogDetailQueryDTO,
    CatalogDTO,
    CreateCatalogDTO,
    PublicCatalogDTO,
    PublicCatalogListDTO,
    PublicCatalogQueryDTO,
    UpdateCatalogDTO,
)
from app.modules.catalogs.exceptions import (
    CatalogAlreadyExistsError,
    CatalogNotFoundError,
    InvalidCatalogMediaError,
)
from app.modules.catalogs.model import Catalog
from app.modules.collections.exceptions import (
    CollectionNotFoundError,
)
from app.modules.media.exceptions import (
    MediaAssetNotFoundError,
    MediaAssetNotReadyError,
)
from app.modules.media.model import MediaAssetStatus, MediaType


class CatalogService(AbstractCatalogService):
    def __init__(
        self, uow: AbstractUnitOfWork, media_upload_service: AbstractMediaUploadService
    ) -> None:
        self.uow = uow
        self.media_upload_service = media_upload_service

    async def list_admin(
        self,
        query: AdminCatalogQueryDTO,
    ) -> AdminCatalogListDTO:
        rows, total = await self.uow.catalogs.list_admin(
            page=query.page,
            page_size=query.page_size,
            search=query.search,
            status=query.status,
            collection_id=query.collection_id,
            sort_order=query.sort_order,
        )

        items = [
            AdminCatalogDTO(
                id=catalog.id,
                collection_id=catalog.collection_id,
                pdf_media_asset_id=catalog.pdf_media_asset_id,
                cover_media_asset_id=catalog.cover_media_asset_id,
                title=catalog.title,
                description=catalog.description,
                pdf_url=pdf_asset.secure_url,
                cover_image_url=cover_asset.secure_url,
                created_at=catalog.created_at,
                status=catalog.status,
                updated_at=catalog.updated_at,
            )
            for catalog, pdf_asset, cover_asset in rows
        ]

        return AdminCatalogListDTO(
            items=items,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=(math.ceil(total / query.page_size) if total else 0),
        )

    async def get_by_id(
        self,
        catalog_id: UUID,
    ) -> CatalogDetailQueryDTO:
        catalog = await self.uow.catalogs.get_by_id(catalog_id)

        if catalog is None:
            raise CatalogNotFoundError(catalog_id)

        return CatalogDetailQueryDTO(
            id=catalog.id,
            collection_id=catalog.collection_id,
            pdf_media_asset_id=catalog.pdf_media_asset_id,
            cover_media_asset_id=catalog.cover_media_asset_id,
            title=catalog.title,
            description=catalog.description,
            status=catalog.status,
            pdf_url=self.media_upload_service.get_asset_url(
                media_asset=catalog.pdf_media_asset,
            ),
            cover_image_url=self.media_upload_service.get_asset_url(
                media_asset=catalog.cover_media_asset,
            ),
            created_at=catalog.created_at,
            updated_at=catalog.updated_at,
        )

    async def get_public_by_collection_id(
        self,
        collection_id: UUID,
    ) -> PublicCatalogDTO | None:
        catalog = await self.uow.catalogs.get_by_collection_id(
            collection_id,
        )

        if catalog is None:
            return None

        media_asset = await self.uow.media_assets.get_by_id(
            catalog.media_asset_id,
        )

        if (
            media_asset is None
            or media_asset.status != MediaAssetStatus.READY
            or media_asset.media_type != MediaType.PDF
            or media_asset.mime_type != "application/pdf"
            or not media_asset.secure_url
        ):
            return None

        return PublicCatalogDTO(
            id=catalog.id,
            collection_id=catalog.collection_id,
            title=catalog.title,
            description=catalog.description,
            catalog_url=media_asset.secure_url,
            created_at=catalog.created_at,
            updated_at=catalog.updated_at,
        )

    async def list_public(
        self,
        query: PublicCatalogQueryDTO,
    ) -> PublicCatalogListDTO:
        rows, total = await self.uow.catalogs.list_public(
            page=query.page,
            page_size=query.page_size,
            search=query.search,
            collection_id=query.collection_id,
            sort_order=query.sort_order,
        )

        items = [
            PublicCatalogDTO(
                id=catalog.id,
                collection_id=catalog.collection_id,
                title=catalog.title,
                description=catalog.description,
                catalog_url=pdf_asset.secure_url,
                cover_image_url=cover_asset.secure_url,
                created_at=catalog.created_at,
                updated_at=catalog.updated_at,
            )
            for catalog, pdf_asset, cover_asset in rows
        ]

        return PublicCatalogListDTO(
            items=items,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=math.ceil(total / query.page_size) if total else 0,
        )

    async def get_by_collection_id(
        self,
        collection_id: UUID,
    ) -> CatalogDTO | None:
        catalog = await self.uow.catalogs.get_by_collection_id(
            collection_id,
        )

        if catalog is None:
            return None

        return self._to_dto(catalog)

    async def create(self, payload: CreateCatalogDTO) -> CatalogDTO:
        collection = await self.uow.collections.get_by_id(
            payload.collection_id,
        )
        if collection is None:
            raise CollectionNotFoundError(payload.collection_id)

        existing_catalog = await self.uow.catalogs.get_by_collection_id(
            payload.collection_id,
        )

        if existing_catalog is not None:
            raise CatalogAlreadyExistsError(payload.collection_id)

        pdf_asset = await self.uow.media_assets.get_by_id(
            payload.pdf_media_asset_id,
        )
        if pdf_asset is None:
            raise MediaAssetNotFoundError(payload.pdf_media_asset_id)

        if pdf_asset.status != MediaAssetStatus.READY:
            raise MediaAssetNotReadyError(pdf_asset.id)

        if (
            pdf_asset.media_type != MediaType.PDF
            or pdf_asset.mime_type != "application/pdf"
            or not pdf_asset.secure_url
        ):
            raise InvalidCatalogMediaError(pdf_asset.id)

        cover_asset = await self.uow.media_assets.get_by_id(
            payload.cover_media_asset_id,
        )
        if cover_asset is None:
            raise MediaAssetNotFoundError(payload.cover_media_asset_id)

        if cover_asset.status != MediaAssetStatus.READY:
            raise MediaAssetNotReadyError(cover_asset.id)

        if (
            cover_asset.media_type != MediaType.IMAGE
            or not cover_asset.mime_type
            or not cover_asset.mime_type.startswith("image/")
            or not cover_asset.secure_url
        ):
            raise InvalidCatalogMediaError(cover_asset.id)

        catalog = Catalog(
            collection_id=payload.collection_id,
            pdf_media_asset_id=payload.pdf_media_asset_id,
            cover_media_asset_id=payload.cover_media_asset_id,
            title=payload.title,
            description=payload.description,
        )

        catalog = await self.uow.catalogs.create(catalog)
        await self.uow.commit()

        return self._to_dto(catalog)

    async def update(
        self,
        catalog_id: UUID,
        payload: UpdateCatalogDTO,
    ) -> CatalogDTO:
        catalog = await self.uow.catalogs.get_by_id(catalog_id)

        if catalog is None:
            raise CatalogNotFoundError(catalog_id)

        old_pdf_media_id = catalog.pdf_media_asset_id
        old_cover_media_id = catalog.cover_media_asset_id

        new_pdf_media_id = old_pdf_media_id
        new_cover_media_id = old_cover_media_id

        # Validate replacement PDF.
        if (
            payload.pdf_media_asset_id is not None
            and payload.pdf_media_asset_id != old_pdf_media_id
        ):
            pdf_asset = await self.uow.media_assets.get_by_id(
                payload.pdf_media_asset_id,
            )

            if pdf_asset is None:
                raise MediaAssetNotFoundError(
                    payload.pdf_media_asset_id,
                )

            if pdf_asset.status != MediaAssetStatus.READY:
                raise MediaAssetNotReadyError(pdf_asset.id)

            if (
                pdf_asset.media_type != MediaType.PDF
                or pdf_asset.mime_type != "application/pdf"
            ):
                raise InvalidCatalogMediaError(pdf_asset.id)

            new_pdf_media_id = pdf_asset.id

        # Validate replacement cover image.
        if (
            payload.cover_media_asset_id is not None
            and payload.cover_media_asset_id != old_cover_media_id
        ):
            cover_asset = await self.uow.media_assets.get_by_id(
                payload.cover_media_asset_id,
            )

            if cover_asset is None:
                raise MediaAssetNotFoundError(
                    payload.cover_media_asset_id,
                )

            if cover_asset.status != MediaAssetStatus.READY:
                raise MediaAssetNotReadyError(cover_asset.id)

            if cover_asset.media_type != MediaType.IMAGE:
                raise InvalidCatalogMediaError(cover_asset.id)

            new_cover_media_id = cover_asset.id

        # Update catalog fields.
        catalog.pdf_media_asset_id = new_pdf_media_id
        catalog.cover_media_asset_id = new_cover_media_id

        if payload.title is not None:
            catalog.title = payload.title

        if payload.description is not None:
            catalog.description = payload.description

        if payload.status is not None:
            catalog.status = payload.status

        await self.uow.catalogs.update(catalog)

        media_ids_to_delete = []

        if old_pdf_media_id is not None and old_pdf_media_id != new_pdf_media_id:
            media_ids_to_delete.append(old_pdf_media_id)

        if (
            old_cover_media_id is not None
            and old_cover_media_id != new_cover_media_id
            and old_cover_media_id not in media_ids_to_delete
        ):
            media_ids_to_delete.append(old_cover_media_id)

        if media_ids_to_delete:
            await self.media_upload_service.mark_for_deletion_many(
                media_asset_ids=media_ids_to_delete,
            )

        await self.uow.commit()

        return await self.get_by_id(catalog_id)

    async def delete(
        self,
        catalog_id: UUID,
    ) -> None:
        catalog = await self.uow.catalogs.get_by_id(catalog_id)

        if catalog is None:
            raise CatalogNotFoundError(catalog_id)

        media_ids_to_delete = list(
            {
                media_id
                for media_id in (
                    catalog.pdf_media_asset_id,
                    catalog.cover_media_asset_id,
                )
                if media_id is not None
            }
        )

        await self.uow.catalogs.delete(catalog)

        if media_ids_to_delete:
            await self.media_upload_service.mark_for_deletion_many(
                media_asset_ids=media_ids_to_delete,
            )
        await self.uow.commit()

    @staticmethod
    def _to_dto(catalog: Catalog) -> CatalogDTO:
        return CatalogDTO(
            id=catalog.id,
            collection_id=catalog.collection_id,
            pdf_media_asset_id=catalog.pdf_media_asset_id,
            cover_media_asset_id=catalog.cover_media_asset_id,
            title=catalog.title,
            status=catalog.status,
            description=catalog.description,
            created_at=catalog.created_at,
            updated_at=catalog.updated_at,
        )
