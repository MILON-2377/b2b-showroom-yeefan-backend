from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.core.contracts.services.category import AbstractCategoryService
from app.core.security.rate_limiter import limiter
from app.modules.categories.dependencies import get_category_service
from app.modules.categories.schemas import (
    PublicCategoryListResponse,
    PublicCategoryResponse,
)

router = APIRouter(
    prefix="/categories",
)


@router.get(
    "",
    response_model=PublicCategoryListResponse,
)
@limiter.limit("120/minute")
async def list_public_categories(
    request: Request,
    service: Annotated[
        AbstractCategoryService,
        Depends(get_category_service),
    ],
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
) -> PublicCategoryListResponse:
    result = await service.list_public(
        page=page,
        page_size=page_size,
    )

    total_pages = ceil(result.total / page_size) if result.total else 0

    return PublicCategoryListResponse(
        items=[PublicCategoryResponse.from_dto(item) for item in result.items],
        total=result.total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
