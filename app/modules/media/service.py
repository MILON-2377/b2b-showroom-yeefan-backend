from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID

from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.storage.media import AbstractMediaStorage
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.storage.cloudinary import (
    CloudinaryAssetVerificationError,
)
from app.modules.media.dtos import CreateUploadIntentDTO, UploadIntent
from app.modules.media.exceptions import (
    MediaAssetNotFoundError,
    MediaAssetVerificationError,
    UploadSessionExpiredError,
    UploadSessionInvalidStateError,
    UploadSessionNotFoundError,
)
from app.modules.media.model import MediaType
from app.shared.utils.storage_key import generate_storage_key

from .exceptions import MediaAssetNotReadyError
from .model import MediaAsset, MediaAssetStatus, UploadSession, UploadSessionStatus


class MediaUploadService(AbstractMediaUploadService):
    def __init__(
        self,
        *,
        uow: AbstractUnitOfWork,
        storage: AbstractMediaStorage,
    ):
        self.uow = uow
        self.storage = storage

    async def create_upload_intent(
        self, payload: CreateUploadIntentDTO
    ) -> UploadIntent:

        storage_key = generate_storage_key(
            namespace=payload.namespace,
            entity_id=payload.entity_id,
        )

        if payload.media_type == MediaType.PDF:
            extension = Path(payload.original_filename or "").suffix.lower()

            if not extension:
                extension = ".pdf"

            if extension != ".pdf":
                raise ValueError("PDF uploads must use a .pdf filename.")

            storage_key = f"{storage_key}{extension}"

        media_asset = await self.uow.media_assets.add(
            MediaAsset(
                storage_provider=payload.storage_provider,
                storage_key=storage_key,
                media_type=payload.media_type.value,
                mime_type=payload.mime_type,
                original_filename=payload.original_filename,
                status=MediaAssetStatus.PENDING,
            )
        )

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=payload.expires_in)

        upload_session = await self.uow.upload_sessions.add(
            UploadSession(
                media_asset_id=media_asset.id,
                status=UploadSessionStatus.PENDING,
                expires_at=expires_at,
            )
        )

        await self.uow.flush()
        await self.uow.commit()

        upload = await self.storage.create_signed_upload(
            public_id=storage_key,
            media_type=payload.media_type,
            mime_type=payload.mime_type,
            expires_in=payload.expires_in,
        )

        return UploadIntent(
            media_asset_id=media_asset.id,
            upload_session_id=upload_session.id,
            storage_key=storage_key,
            upload_url=upload.upload_url,
            upload_params=upload.upload_params,
        )

    async def finalize_upload(
        self,
        *,
        upload_session_id: UUID,
    ) -> MediaAsset:
        upload_session = await self.uow.upload_sessions.get_by_id(upload_session_id)

        if upload_session is None:
            raise UploadSessionNotFoundError(upload_session_id)

        if upload_session.status != UploadSessionStatus.PENDING:
            raise UploadSessionInvalidStateError(upload_session_id)

        now = datetime.now(timezone.utc)

        if upload_session.expires_at <= now:
            upload_session.status = UploadSessionStatus.EXPIRED

            await self.uow.commit()

            raise UploadSessionExpiredError(upload_session_id)

        media_asset = await self.uow.media_assets.get_by_id(
            upload_session.media_asset_id
        )

        if media_asset is None:
            raise MediaAssetNotFoundError(upload_session.media_asset_id)

        storage_key = media_asset.storage_key
        media_type = media_asset.media_type
        mime_type = media_asset.mime_type
        media_asset_id = media_asset.id

        await self.uow.commit()

        try:
            verified = await self.storage.verify_asset(
                public_id=storage_key,
                media_type=MediaType(media_type),
                expected_mime_type=mime_type,
            )
        except CloudinaryAssetVerificationError as exc:
            print(f"Media verification failed: {exc!r}")
            raise MediaAssetVerificationError(
                f"Media asset verification failed: {exc}"
            ) from exc
        except Exception:
            self.uow.rollback()
            raise

        if not verified.secure_url:
            raise MediaAssetVerificationError(
                f"Cloudinary asset '{storage_key}' has no secure URL"
            )

        upload_session = await self.uow.upload_sessions.get_by_id(upload_session_id)

        if upload_session is None:
            raise UploadSessionNotFoundError(upload_session_id)

        if upload_session.status != UploadSessionStatus.PENDING:
            raise UploadSessionInvalidStateError(upload_session_id)

        media_asset = await self.uow.media_assets.get_by_id(
            upload_session.media_asset_id
        )

        if media_asset is None:
            raise MediaAssetNotFoundError(upload_session.media_asset_id)

        media_asset.status = MediaAssetStatus.READY
        media_asset.file_size = verified.file_size
        media_asset.width = verified.width
        media_asset.height = verified.height
        media_asset.duration = verified.duration
        media_asset.secure_url = verified.secure_url

        upload_session.status = UploadSessionStatus.COMPLETED

        await self.uow.commit()

        return media_asset

    def get_asset_url(
        self,
        *,
        media_asset: MediaAsset,
    ) -> str:

        if not media_asset.secure_url:
            raise MediaAssetNotReadyError(media_asset.id)

        return media_asset.secure_url

    async def mark_for_deletion(
        self,
        *,
        media_asset: MediaAsset,
    ) -> None:
        if media_asset.status == MediaAssetStatus.DELETED:
            return

        if media_asset.status != MediaAssetStatus.READY:
            raise MediaAssetNotReadyError(media_asset.id)

        media_asset.status = MediaAssetStatus.DELETION_PENDING

        await self.uow.media_assets.update(media_asset)

    async def mark_for_deletion_many(
        self,
        *,
        media_asset_ids: list[UUID],
    ) -> None:
        media_assets = await self.uow.media_assets.get_by_ids(
            media_asset_ids=media_asset_ids,
        )

        media_assets_by_id = {
            media_asset.id: media_asset for media_asset in media_assets
        }

        for media_asset_id in media_asset_ids:
            if media_asset_id not in media_assets_by_id:
                raise MediaAssetNotFoundError(media_asset_id)

        await self.uow.media_assets.mark_for_deletion_many(
            list(media_assets_by_id.values())
        )
