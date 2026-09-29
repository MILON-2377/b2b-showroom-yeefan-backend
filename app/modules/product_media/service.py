from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.storage.interface import AbstractObjectStorage
from app.modules.media.model import (
    MediaAsset,
    MediaAssetStatus,
    UploadSession,
    UploadSessionStatus,
)
from app.modules.product_media.dto import UploadIntent
from app.shared.utils.storage_key import generate_storage_key

from .model import ProductMedia


class ProductMediaService:
    def __init__(
        self,
        *,
        uow: AbstractUnitOfWork,
        storage: AbstractObjectStorage,
    ):
        self.uow = uow
        self.storage = storage

    async def create_upload_intent(
        self,
        *,
        storage_provider: str,
        product_id: UUID,
        media_type: str,
        mime_type: str,
        original_filename: str | None = None,
        expires_in: int = 900,
    ) -> UploadIntent:

        storage_key = generate_storage_key(
            namespace="products/media",
            entity_id=product_id,
            filename=original_filename or "",
        )

        media_asset = MediaAsset(
            storage_provider=storage_provider,
            storage_key=storage_key,
            media_type=media_type,
            mime_type=mime_type,
            original_filename=original_filename,
            status=MediaAssetStatus.PENDING,
        )

        self.uow.media_assets.add(media_asset)

        await self.uow.flush()

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        upload_session = UploadSession(
            product_id=product_id,
            media_asset_id=media_asset.id,
            status=UploadSessionStatus.PENDING,
            expires_at=expires_at,
        )

        self.uow.upload_sessions.add(upload_session)

        upload_url = await self.storage.create_presigned_upload_url(
            storage_key=storage_key,
            mime_type=mime_type,
            expires_in=expires_in,
        )

        await self.uow.commit()

        return UploadIntent(
            media_asset_id=media_asset.id,
            upload_session_id=upload_session.id,
            storage_key=storage_key,
            upload_url=upload_url,
        )

    async def finalize_upload(
        self,
        *,
        upload_session_id: UUID,
        alt_text: str | None = None,
        sort_order: int = 0,
        is_primary: bool = False,
    ) -> ProductMedia:
        upload_session = await self.uow.upload_sessions.get_by_id(upload_session_id)

        if upload_session is None:
            raise ValueError("Upload session not found")

        if upload_session.status != UploadSessionStatus.PENDING:
            raise ValueError("Upload session is not pending")

        now = datetime.now(timezone.utc)

        if upload_session.expires_at <= now:
            upload_session.status = UploadSessionStatus.EXPIRED
            await self.uow.commit()
            raise ValueError("Upload session has expired")

        media_asset = await self.uow.media_assets.get_by_id(
            upload_session.media_asset_id
        )

        if media_asset is None:
            raise ValueError("Media asset not found")

        metadata = await self.storage.get_object_metadata(
            storage_key=media_asset.storage_key,
        )

        if metadata is None:
            raise ValueError("Uploaded object not found")

        if metadata.mime_type != media_asset.mime_type:
            raise ValueError(
                "Uploaded object MIME type does not match expected MIME type"
            )

        media_asset.status = MediaAssetStatus.READY
        media_asset.file_size = metadata.size

        upload_session.status = UploadSessionStatus.COMPLETED

        product_media = ProductMedia(
            product_id=upload_session.product_id,
            media_asset_id=media_asset.id,
            alt_text=alt_text,
            sort_order=sort_order,
            is_primary=is_primary,
        )

        self.uow.product_media.add(product_media)

        await self.uow.commit()

        return product_media
