from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.about_videos.dtos import (
    AboutVideoDTO,
    CreateAboutVideoDTO,
    UpdateAboutVideoDTO,
)

from app.core.models import RecordStatus


class AbstractAboutVideoService(ABC):
    @abstractmethod
    async def create(
        self,
        data: CreateAboutVideoDTO,
    ) -> AboutVideoDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        video_id: UUID,
    ) -> AboutVideoDTO:
        raise NotImplementedError

    @abstractmethod
    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[AboutVideoDTO], int]:
        raise NotImplementedError

    @abstractmethod
    async def list_published(self) -> list[AboutVideoDTO]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        video_id: UUID,
        data: UpdateAboutVideoDTO,
    ) -> AboutVideoDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        video_id: UUID,
    ) -> None:
        raise NotImplementedError
