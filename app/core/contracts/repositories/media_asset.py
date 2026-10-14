from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.media.dtos import MediaAssetDeletionItem
from app.modules.media.model import MediaAsset, MediaAssetStatus


class AbstractMediaAssetRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        media_asset_id: UUID,
    ) -> MediaAsset | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(
        self,
        media_asset_ids: list[UUID],
    ) -> list[MediaAsset]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_storage_key(
        self,
        storage_provider: str,
        storage_key: str,
    ) -> MediaAsset | None:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        *,
        status: MediaAssetStatus | None = None,
    ) -> list[MediaAsset]:
        raise NotImplementedError

    @abstractmethod
    async def add(
        self,
        media_asset: MediaAsset,
    ) -> MediaAsset:
        raise NotImplementedError

    @abstractmethod
    async def update(self, media_asset: MediaAsset) -> MediaAsset:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        media_asset: MediaAsset,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_deletion_pending(
        self,
        *,
        limit: int = 100,
    ) -> list[MediaAssetDeletionItem]:
        raise NotImplementedError

    @abstractmethod
    async def mark_for_deletion_many(
        self,
        media_assets: list[MediaAsset],
    ) -> list[MediaAsset]:
        raise NotImplementedError
