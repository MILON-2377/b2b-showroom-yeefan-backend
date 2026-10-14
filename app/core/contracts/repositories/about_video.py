from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.about_videos.model import AboutVideo


class AbstractAboutVideoRepository(ABC):
    @abstractmethod
    async def create(
        self,
        video: AboutVideo,
    ) -> AboutVideo:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        video_id: UUID,
    ) -> AboutVideo | None:
        raise NotImplementedError

    @abstractmethod
    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[AboutVideo], int]:
        raise NotImplementedError

    @abstractmethod
    async def list_published(self) -> list[AboutVideo]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, video: AboutVideo) -> AboutVideo:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        video: AboutVideo,
    ) -> None:
        raise NotImplementedError
