from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.modules.media.model import UploadSession, UploadSessionStatus


class AbstractUploadSessionRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        upload_session_id: UUID,
    ) -> UploadSession | None: ...

    @abstractmethod
    async def get_by_media_asset_id(
        self,
        media_asset_id: UUID,
    ) -> UploadSession | None: ...

    @abstractmethod
    async def list_expired(
        self,
        *,
        now: datetime,
    ) -> list[UploadSession]: ...

    @abstractmethod
    async def add(
        self,
        upload_session: UploadSession,
    ) -> None: ...

    @abstractmethod
    async def delete(
        self,
        upload_session: UploadSession,
    ) -> None: ...
