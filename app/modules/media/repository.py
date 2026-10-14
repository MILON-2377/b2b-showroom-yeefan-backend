from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.media_asset import AbstractMediaAssetRepository
from app.core.contracts.repositories.upload_session import (
    AbstractUploadSessionRepository,
)

from .dtos import MediaAssetDeletionItem
from .model import MediaAsset, MediaAssetStatus, UploadSession, UploadSessionStatus


class MediaAssetRepository(AbstractMediaAssetRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        media_asset_id: UUID,
    ) -> MediaAsset | None:
        statement = select(MediaAsset).where(MediaAsset.id == media_asset_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_ids(
        self,
        media_asset_ids: list[UUID],
    ) -> list[MediaAsset]:
        if not media_asset_ids:
            return []

        result = await self.session.scalars(
            select(MediaAsset).where(MediaAsset.id.in_(media_asset_ids))
        )

        return list(result)

    async def get_by_storage_key(
        self,
        storage_provider: str,
        storage_key: str,
    ) -> MediaAsset | None:
        statement = select(MediaAsset).where(
            MediaAsset.storage_provider == storage_provider,
            MediaAsset.storage_key == storage_key,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        status: MediaAssetStatus | None = None,
    ) -> list[MediaAsset]:
        statement = select(MediaAsset).order_by(MediaAsset.created_at)

        if status is not None:
            statement = statement.where(MediaAsset.status == status)

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def add(
        self,
        media_asset: MediaAsset,
    ) -> MediaAsset:
        self.session.add(media_asset)
        await self.session.flush()
        return media_asset

    async def delete(
        self,
        media_asset: MediaAsset,
    ) -> None:
        await self.session.delete(media_asset)

    async def update(self, media_asset: MediaAsset) -> MediaAsset:
        self.session.add(media_asset)
        await self.session.flush()
        return media_asset

    async def get_deletion_pending(
        self,
        *,
        limit: int = 100,
    ) -> list[MediaAssetDeletionItem]:
        statement = (
            select(
                MediaAsset.id,
                MediaAsset.storage_key,
                MediaAsset.media_type,
            )
            .where(MediaAsset.status == MediaAssetStatus.DELETION_PENDING)
            .order_by(MediaAsset.created_at)
            .limit(limit)
        )

        result = await self.session.execute(statement)

        return [
            MediaAssetDeletionItem(
                id=row.id,
                storage_key=row.storage_key,
                media_type=row.media_type,
            )
            for row in result.all()
        ]

    async def mark_for_deletion_many(
        self,
        media_assets: list[MediaAsset],
    ) -> list[MediaAsset]:
        for media_asset in media_assets:
            media_asset.status = MediaAssetStatus.DELETION_PENDING

        await self.session.flush()

        return media_assets


class UploadSessionRepository(AbstractUploadSessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        upload_session_id: UUID,
    ) -> UploadSession | None:
        result = await self.session.execute(
            select(UploadSession).where(UploadSession.id == upload_session_id)
        )
        return result.scalar_one_or_none()

    async def get_by_media_asset_id(
        self,
        media_asset_id: UUID,
    ) -> UploadSession | None:
        result = await self.session.execute(
            select(UploadSession).where(UploadSession.media_asset_id == media_asset_id)
        )
        return result.scalar_one_or_none()

    async def list_expired(
        self,
        *,
        now: datetime,
    ) -> list[UploadSession]:
        result = await self.session.execute(
            select(UploadSession)
            .where(
                UploadSession.status == UploadSessionStatus.PENDING,
                UploadSession.expires_at <= now,
            )
            .order_by(UploadSession.expires_at)
        )

        return list(result.scalars().all())

    async def add(
        self,
        upload_session: UploadSession,
    ) -> None:
        self.session.add(upload_session)
        await self.session.flush()
        return upload_session

    async def delete(
        self,
        upload_session: UploadSession,
    ) -> None:
        await self.session.delete(upload_session)
