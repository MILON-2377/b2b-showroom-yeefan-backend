from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.media.dtos import CreateUploadIntentDTO, UploadIntent
from app.modules.media.model import MediaAsset


class AbstractMediaUploadService(ABC):
    @abstractmethod
    async def create_upload_intent(
        self, payload: CreateUploadIntentDTO
    ) -> UploadIntent:
        raise NotImplementedError

    @abstractmethod
    async def finalize_upload(
        self,
        *,
        upload_session_id: UUID,
    ) -> MediaAsset:
        raise NotImplementedError

    @abstractmethod
    def get_asset_url(
        self,
        *,
        media_asset: MediaAsset,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def mark_for_deletion(
        self,
        *,
        media_asset: MediaAsset,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def mark_for_deletion_many(
        self,
        media_asset_ids: list[UUID],
    ) -> None:
        raise NotImplementedError
