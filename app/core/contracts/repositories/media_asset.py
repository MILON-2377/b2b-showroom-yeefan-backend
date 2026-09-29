from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.media.model import MediaAsset, MediaAssetStatus


class AbstractMediaAssetRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        media_asset_id: UUID,
    ) -> MediaAsset | None: ...

    @abstractmethod
    async def get_by_storage_key(
        self,
        storage_provider: str,
        storage_key: str,
    ) -> MediaAsset | None: ...

    @abstractmethod
    async def list(
        self,
        *,
        status: MediaAssetStatus | None = None,
    ) -> list[MediaAsset]: ...

    @abstractmethod
    async def add(
        self,
        media_asset: MediaAsset,
    ) -> MediaAsset: ...

    @abstractmethod
    async def delete(
        self,
        media_asset: MediaAsset,
    ) -> None: ...
