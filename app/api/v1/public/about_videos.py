from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.core.contracts.services.about_video import AbstractAboutVideoService
from app.core.security.rate_limiter import limiter
from app.modules.about_videos.dependencies import get_about_video_service
from app.modules.about_videos.schemas import AboutVideoResponse

router = APIRouter(
    prefix="/about-videos",
)


@router.get(
    "",
    response_model=list[AboutVideoResponse],
)
@limiter.limit("120/minute")
async def list_public_about_videos(
    request: Request,
    service: Annotated[
        AbstractAboutVideoService,
        Depends(get_about_video_service),
    ],
) -> list[AboutVideoResponse]:
    videos = await service.list_published()

    return [AboutVideoResponse.model_validate(video) for video in videos]
