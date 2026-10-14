from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response, status

from app.core.contracts.services.about_video import (
    AbstractAboutVideoService,
)
from app.core.models import RecordStatus
from app.core.security.rate_limiter import limiter
from app.modules.about_videos.dependencies import get_about_video_service
from app.modules.about_videos.schemas import (
    AboutVideoListResponse,
    AboutVideoResponse,
    CreateAboutVideoRequest,
    UpdateAboutVideoRequest,
)

router = APIRouter(
    prefix="/about-videos",
    tags=["admin-about-videos"],
)


@router.post(
    "",
    response_model=AboutVideoResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
async def create_about_video(
    request: Request,
    payload: CreateAboutVideoRequest,
    service: Annotated[
        AbstractAboutVideoService,
        Depends(get_about_video_service),
    ],
) -> AboutVideoResponse:
    video = await service.create(payload.to_dto())
    return AboutVideoResponse.model_validate(video)


@router.get(
    "",
    response_model=AboutVideoListResponse,
)
@limiter.limit("120/minute")
async def list_about_videos(
    request: Request,
    service: Annotated[
        AbstractAboutVideoService,
        Depends(get_about_video_service),
    ],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    video_status: RecordStatus | None = Query(None, alias="status"),
) -> AboutVideoListResponse:
    items, total = await service.list_admin(
        page=page,
        page_size=page_size,
        search=search,
        status=video_status,
    )

    return AboutVideoListResponse(
        items=[AboutVideoResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get(
    "/{video_id}",
    response_model=AboutVideoResponse,
)
@limiter.limit("120/minute")
async def get_about_video(
    request: Request,
    video_id: UUID,
    service: Annotated[
        AbstractAboutVideoService,
        Depends(get_about_video_service),
    ],
) -> AboutVideoResponse:
    video = await service.get_by_id(video_id)
    return AboutVideoResponse.model_validate(video)


@router.patch(
    "/{video_id}",
    response_model=AboutVideoResponse,
)
@limiter.limit("30/minute")
async def update_about_video(
    request: Request,
    video_id: UUID,
    payload: UpdateAboutVideoRequest,
    service: Annotated[
        AbstractAboutVideoService,
        Depends(get_about_video_service),
    ],
) -> AboutVideoResponse:
    video = await service.update(
        video_id=video_id,
        data=payload.to_dto(),
    )
    return AboutVideoResponse.model_validate(video)


@router.delete(
    "/{video_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("10/minute")
async def delete_about_video(
    request: Request,
    video_id: UUID,
    service: Annotated[
        AbstractAboutVideoService,
        Depends(get_about_video_service),
    ],
) -> Response:
    await service.delete(video_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
