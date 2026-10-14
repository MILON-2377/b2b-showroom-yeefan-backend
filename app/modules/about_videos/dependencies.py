from typing import Annotated

from fastapi import Depends

from app.core.contracts.services.about_video import AbstractAboutVideoService
from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.about_videos.service import AboutVideoService
from app.modules.media.dependencies import get_media_upload_service
from app.shared.dependencies import get_uow


def get_about_video_service(
    uow: Annotated[AbstractUnitOfWork, Depends(get_uow)],
    media_upload_service: Annotated[
        AbstractMediaUploadService, Depends(get_media_upload_service)
    ],
) -> AbstractAboutVideoService:
    return AboutVideoService(uow=uow, media_upload_service=media_upload_service)
