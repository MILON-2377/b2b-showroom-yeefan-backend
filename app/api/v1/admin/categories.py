from math import ceil
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from app.core.contracts.services.category import AbstractCategoryService
from app.core.models import RecordStatus
from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.core.security.rate_limiter import limiter
from app.modules.auth.dtos.auth_context import AuthContext
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
    request: Request,
    payload: CreateCategoryRequest,
    service: Annotated[
        AbstractCategoryService,
        Depends(get_category_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATEGORY_MANAGE)),
    ],
) -> CategoryResponse:
    category_payload = CreateCategoryDTO(
        name=payload.name,
        description=payload.description,
        status=payload.status,
        image_media_id=payload.image_media_id,
    )

    category = await service.create(
        payload=category_payload,
    )

    return CategoryResponse.from_dto(category)


@router.get(
    "",
    response_model=CategoryListResponse,
)
@limiter.limit("120/minute")
async def list_categories(
    request: Request,
    service: Annotated[
        AbstractCategoryService,
        Depends(get_category_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATEGORY_READ)),
    ],
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
    service: Annotated[
        AbstractCategoryService,
        Depends(get_category_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATEGORY_READ)),
    ],
) -> CategoryResponse:
    category = await service.get_by_slug(slug)

    return CategoryResponse.model_validate(category)


@router.get("/{category_id}", response_model=CategoryResponse)
@limiter.limit("120/minute")
async def get_category_by_id(
    request: Request,
    category_id: UUID,
    service: Annotated[
        AbstractCategoryService,
        Depends(get_category_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATEGORY_READ)),
    ],
) -> CategoryResponse:
    category = await service.get_by_id(category_id)

    return CategoryResponse.model_validate(category)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
@limiter.limit("30/minute")
async def update_category(
    request: Request,
    category_id: UUID,
    payload: UpdateCategoryRequest,
    service: Annotated[
        AbstractCategoryService,
        Depends(get_category_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATEGORY_MANAGE)),
    ],
) -> CategoryResponse:
    category_payload = UpdateCategoryDTO(
        name=payload.name,
        description=payload.description,
        status=payload.status,
        image_media_id=payload.image_media_id,
    )

    category = await service.update(
        category_id=category_id,
        payload=category_payload,
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
    service: Annotated[
        AbstractCategoryService,
        Depends(get_category_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATEGORY_MANAGE)),
    ],
) -> None:
    await service.delete(category_id)
