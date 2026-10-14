from uuid import UUID

from app.core.contracts.services.about_video import (
    AbstractAboutVideoService,
)
from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.about_videos.dtos import (
    AboutVideoDTO,
    CreateAboutVideoDTO,
    UpdateAboutVideoDTO,
)
from app.modules.about_videos.exceptions import (
    AboutVideoMediaValidationError,
    AboutVideoNotFoundError,
)
from app.modules.about_videos.model import AboutVideo
from app.modules.media.exceptions import (
    MediaAssetNotFoundError,
    MediaAssetNotReadyError,
)
from app.modules.media.model import MediaAsset, MediaAssetStatus, MediaType


class AboutVideoService(AbstractAboutVideoService):
    def __init__(
        self, uow: AbstractUnitOfWork, media_upload_service: AbstractMediaUploadService
    ):
        self.uow = uow
        self.media_upload_service = media_upload_service

    def _to_dto(self, video: AboutVideo) -> AboutVideoDTO:
        return AboutVideoDTO(
            id=video.id,
            title=video.title,
            description=video.description,
            media_asset_id=video.media_asset_id,
            video_url=self.media_upload_service.get_asset_url(
                media_asset=video.media_asset,
            ),
            sort_order=video.sort_order,
            status=video.status,
            created_at=video.created_at,
            updated_at=video.updated_at,
        )

    async def _get_ready_video_asset(
        self,
        media_asset_id: UUID,
    ) -> MediaAsset:
        media_asset = await self.uow.media_assets.get_by_id(media_asset_id)

        if media_asset is None:
            raise MediaAssetNotFoundError(media_asset_id)

        if media_asset.status != MediaAssetStatus.READY:
            raise MediaAssetNotReadyError(media_asset_id)

        if media_asset.media_type != MediaType.VIDEO.value:
            raise AboutVideoMediaValidationError(
                "The selected media asset must be a video."
            )

        return media_asset

    async def create(
        self,
        data: CreateAboutVideoDTO,
    ) -> AboutVideoDTO:
        media_asset = await self._get_ready_video_asset(
            data.media_asset_id,
        )

        video = AboutVideo(
            title=data.title,
            description=data.description,
            media_asset_id=media_asset.id,
            sort_order=data.sort_order,
            status=data.status,
        )

        await self.uow.about_videos.create(video)

        await self.uow.commit()

        return AboutVideoDTO(
            id=video.id,
            title=video.title,
            description=video.description,
            media_asset_id=media_asset.id,
            video_url=self.media_upload_service.get_asset_url(
                media_asset=media_asset,
            ),
            sort_order=video.sort_order,
            status=video.status,
            created_at=video.created_at,
            updated_at=video.updated_at,
        )

    async def get_by_id(
        self,
        video_id: UUID,
    ) -> AboutVideoDTO:

        video = await self.uow.about_videos.get_by_id(video_id)

        if video is None:
            raise AboutVideoNotFoundError(video_id)

        return self._to_dto(video)

    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[AboutVideoDTO], int]:

        videos, total = await self.uow.about_videos.list_admin(
            page=page,
            page_size=page_size,
            search=search,
            status=status,
        )

        return [self._to_dto(video) for video in videos], total

    async def list_published(self) -> list[AboutVideoDTO]:
        videos = await self.uow.about_videos.list_published()

        return [self._to_dto(video) for video in videos]

    async def update(
        self,
        video_id: UUID,
        data: UpdateAboutVideoDTO,
    ) -> AboutVideoDTO:

        video = await self.uow.about_videos.get_by_id(video_id)

        if video is None:
            raise AboutVideoNotFoundError(video_id)

        if data.media_asset_id is not None:
            await self._get_ready_video_asset(data.media_asset_id)
            video.media_asset_id = data.media_asset_id

        if data.title is not None:
            video.title = data.title

        if data.description is not None:
            video.description = data.description

        if data.sort_order is not None:
            video.sort_order = data.sort_order

        if data.status is not None:
            video.status = data.status

        video = await self.uow.about_videos.update(video)
        await self.uow.commit()

        return self._to_dto(video)

    async def delete(self, video_id: UUID) -> None:
        video = await self.uow.about_videos.get_by_id(video_id)

        if video is None:
            raise AboutVideoNotFoundError(video_id)

        media_asset = await self.uow.media_assets.get_by_id(
            video.media_asset_id
        )

        if media_asset is not None:
            await self.media_upload_service.mark_for_deletion(
                media_asset=media_asset,
            )

        await self.uow.about_videos.delete(video)
        await self.uow.commit()