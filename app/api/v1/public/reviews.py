from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from app.core.contracts.services.review import AbstractReviewService
from app.core.security.rate_limiter import limiter
from app.modules.reviews.dependencies import get_review_service
from app.modules.reviews.dtos import CreateReviewDTO
from app.modules.reviews.schemas import (
    CreateReviewRequest,
    PublicReviewListResponse,
    PublicReviewResponse,
    ReviewResponse,
)

router = APIRouter(
    prefix="/reviews",
)


@router.post(
    "",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_review(
    request: Request,
    payload: CreateReviewRequest,
    service: Annotated[
        AbstractReviewService,
        Depends(
            get_review_service,
        ),
    ],
) -> ReviewResponse:
    dto = CreateReviewDTO(
        name=payload.name,
        company_name=payload.company_name,
        job_title=payload.job_title,
        country=payload.country,
        rating=payload.rating,
        message=payload.message,
        product_id=payload.product_id,
        avatar_media_id=payload.avatar_media_id,
    )

    result = await service.create(dto)

    return ReviewResponse.from_dto(result)


@router.get(
    "",
    response_model=PublicReviewListResponse,
)
@limiter.limit("120/minute")
async def list_public_reviews(
    request: Request,
    service: Annotated[
        AbstractReviewService,
        Depends(
            get_review_service,
        ),
    ],
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=6,
        ge=1,
        le=100,
    ),
) -> PublicReviewListResponse:
    result = await service.list_public(
        page=page,
        page_size=page_size,
    )

    total_pages = ceil(result.total / page_size) if result.total else 0

    return PublicReviewListResponse(
        items=[PublicReviewResponse.from_dto(item) for item in result.items],
        total=result.total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
