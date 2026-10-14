from math import ceil
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from app.core.contracts.services.category import AbstractCategoryService
from app.core.models import RecordStatus
from app.core.security.rate_limiter import limiter
from app.modules.categories.dependencies import get_category_service
from app.modules.categories.dtos import CreateCategoryDTO, UpdateCategoryDTO
from app.modules.categories.schemas import (
    CategoryListItemResponse,
    CategoryListResponse,
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("60/minute")
async def create_category(
    
    request: CreateCategoryRequest,
    service: AbstractCategoryService = Depends(get_category_service),
) -> CategoryResponse:
    payload = CreateCategoryDTO(
        name=request.name,
        description=request.description,
        status=request.status,
        image_media_id=request.image_media_id,
    )

    category = await service.create(
        payload=payload,
    )

    return CategoryResponse.from_dto(category)


@router.get(
    "",
    response_model=CategoryListResponse,
)
@limiter.limit("120/minute")
async def list_categories(
    request: Request,
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=255,
    ),
    status_filter: RecordStatus | None = Query(
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
    service: AbstractCategoryService = Depends(get_category_service),
) -> CategoryListResponse:
    result = await service.list(
        search=search,
        status=status_filter,
        page=page,
        page_size=page_size,
    )

    total_pages = ceil(result.total / page_size) if result.total else 0

    return CategoryListResponse(
        items=[CategoryListItemResponse.model_validate(item) for item in result.items],
        total=result.total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/slug/{slug}",
    response_model=CategoryResponse,
)
@limiter.limit("120/minute")
async def get_category_by_slug(
    request: Request,
    slug: str,
    service: AbstractCategoryService = Depends(get_category_service),
) -> CategoryResponse:
    category = await service.get_by_slug(slug)

    return CategoryResponse.model_validate(category)


@router.get("/{category_id}", response_model=CategoryResponse)
@limiter.limit("120/minute")
async def get_category_by_id(
    request: Request,
    category_id: UUID,
    service: AbstractCategoryService = Depends(get_category_service),
) -> CategoryResponse:
    category = await service.get_by_id(category_id)

    return CategoryResponse.model_validate(category)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
@limiter.limit("30/minute")
async def update_category(
    
    category_id: UUID,
    request: UpdateCategoryRequest,
    service: AbstractCategoryService = Depends(get_category_service),
) -> CategoryResponse:
    payload = UpdateCategoryDTO(
        name=request.name,
        description=request.description,
        status=request.status,
        image_media_id=request.image_media_id,
    )

    category = await service.update(
        category_id=category_id,
        payload=payload,
    )

    return CategoryResponse.from_dto(category)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("10/minute")
async def delete_category(
    request: Request,
    category_id: UUID,
    service: AbstractCategoryService = Depends(get_category_service),
) -> None:
    await service.delete(category_id)
