from math import ceil
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from app.core.contracts.services.review import AbstractReviewService
from app.core.security.rate_limiter import limiter
from app.modules.reviews.dependencies import get_review_service
from app.modules.reviews.dtos import (
    UpdateReviewDTO,
    UpdateReviewNotesDTO,
    UpdateReviewStatusDTO,
)
from app.modules.reviews.model import ReviewStatus
from app.modules.reviews.schemas import (
    ReviewListResponse,
    ReviewResponse,
    UpdateReviewNotesRequest,
    UpdateReviewRequest,
    UpdateReviewStatusRequest,
)

router = APIRouter(
    prefix="/reviews",
    tags=["admin-reviews"]
)


@router.get(
    "",
    response_model=ReviewListResponse,
)
@limiter.limit("120/minute")
async def list_reviews(
    request: Request,
    status_filter: ReviewStatus | None = Query(
        default=None,
        alias="status",
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    service: AbstractReviewService = Depends(
        get_review_service,
    ),
) -> ReviewListResponse:
    result = await service.list(
        status=status_filter,
        page=page,
        page_size=page_size,
    )

    total_pages = ceil(result.total / page_size) if result.total else 0

    return ReviewListResponse(
        items=[ReviewResponse.from_dto(item) for item in result.items],
        total=result.total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
@limiter.limit("120/minute")
async def get_review(
    request: Request,
    review_id: UUID,
    service: AbstractReviewService = Depends(
        get_review_service,
    ),
) -> ReviewResponse:
    result = await service.get_by_id(review_id)

    return ReviewResponse.from_dto(result)


@router.patch(
    "/{review_id}",
    response_model=ReviewResponse,
)
@limiter.limit("60/minute")
async def update_review(
    request: Request,
    review_id: UUID,
    payload: UpdateReviewRequest,
    service: AbstractReviewService = Depends(
        get_review_service,
    ),
) -> ReviewResponse:
    dto = UpdateReviewDTO(
        name=payload.name,
        company_name=payload.company_name,
        job_title=payload.job_title,
        country=payload.country,
        rating=payload.rating,
        message=payload.message,
        product_id=payload.product_id,
        avatar_media_id=payload.avatar_media_id,
    )

    result = await service.update(
        review_id,
        dto,
    )

    return ReviewResponse.from_dto(result)


@router.patch(
    "/{review_id}/status",
    response_model=ReviewResponse,
)
@limiter.limit("60/minute")
async def update_review_status(
    request: Request,
    review_id: UUID,
    payload: UpdateReviewStatusRequest,
    service: AbstractReviewService = Depends(
        get_review_service,
    ),
) -> ReviewResponse:
    dto = UpdateReviewStatusDTO(
        status=payload.status,
    )

    result = await service.update_status(
        review_id,
        dto,
    )

    return ReviewResponse.from_dto(result)


@router.patch(
    "/{review_id}/notes",
    response_model=ReviewResponse,
)
@limiter.limit("60/minute")
async def update_review_notes(
    request: Request,
    review_id: UUID,
    payload: UpdateReviewNotesRequest,
    service: AbstractReviewService = Depends(
        get_review_service,
    ),
) -> ReviewResponse:
    dto = UpdateReviewNotesDTO(
        internal_notes=payload.internal_notes,
    )

    result = await service.update_notes(
        review_id,
        dto,
    )

    return ReviewResponse.from_dto(result)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("10/minute")
async def delete_review(
    request: Request,
    review_id: UUID,
    service: AbstractReviewService = Depends(
        get_review_service,
    ),
) -> None:
    await service.delete(review_id)
