from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.core.contracts.services.brand import AbstractBrandService
from app.core.security.rate_limiter import limiter
from app.modules.brands.dependencies import get_brand_service
from app.modules.brands.dtos import PublicBrandQueryDTO
from app.modules.brands.schemas import (
    PublicBrandListResponse,
    PublicBrandQueryParams,
    PublicBrandResponse,
)

router = APIRouter(prefix="/brands")


@router.get(
    "",
    response_model=PublicBrandListResponse,
)
@limiter.limit("120/minute")
async def list_public_brands(
    request: Request,
    params: Annotated[
        PublicBrandQueryParams,
        Depends(),
    ],
    service: Annotated[
        AbstractBrandService,
        Depends(get_brand_service),
    ],
) -> PublicBrandListResponse:
    result = await service.list_public(
        PublicBrandQueryDTO(
            page=params.page,
            page_size=params.page_size,
            search=params.search,
        )
    )

    return PublicBrandListResponse(
        items=[
            PublicBrandResponse(
                id=item.id,
                name=item.name,
                slug=item.slug,
                description=item.description,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in result.items
        ],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        total_pages=result.total_pages,
    )
