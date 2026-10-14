from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from app.core.contracts.services.brand import AbstractBrandService
from app.core.errors.schemas import DeleteResponse
from app.core.models import RecordStatus
from app.core.security.rate_limiter import limiter
from app.modules.brands.dependencies import get_brand_service
from app.modules.brands.query import BrandListQuery
from app.modules.brands.schemas import (
    BrandListResponse,
    BrandResponse,
    CreateBrandRequest,
    UpdateBrandRequest,
)
from app.modules.brands.service import BrandService

router = APIRouter(
    prefix="/brands",
    tags=["admin-brands"],
)


@router.post(
    "/create",
    response_model=BrandResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("60/minute")
async def create_brand(
    request: Request,
    payload: CreateBrandRequest,
    service: BrandService = Depends(get_brand_service),
) -> BrandResponse:
    brand = await service.create(
        name=payload.name,
        description=payload.description,
    )

    return BrandResponse(
        id=brand.id,
        name=brand.name,
        slug=brand.slug,
        description=brand.description,
        logo_media_url=brand.logo_media_url,
        status=brand.status.value,
        created_at=brand.created_at,
        updated_at=brand.updated_at,
    )


@router.get("/", response_model=BrandListResponse)
@limiter.limit("120/minute")
async def list_brands(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, min_length=1),
    status: RecordStatus | None = Query(default=None),
    service: AbstractBrandService = Depends(get_brand_service),
) -> BrandListResponse:

    query = BrandListQuery(
        page=page,
        page_size=page_size,
        search=search,
        status=status,
    )

    result = await service.list(query)

    return BrandListResponse(
        items=[
            BrandResponse(
                id=brand.id,
                name=brand.name,
                slug=brand.slug,
                description=brand.description,
                logo_media_url=brand.logo_media_url,
                status=brand.status.value,
                created_at=brand.created_at,
                updated_at=brand.updated_at,
            )
            for brand in result.items
        ],
        total=result.total,
        page=page,
        page_size=page_size,
    )


@router.get("/{brand_id}", response_model=BrandResponse)
@limiter.limit("60/minute")
async def getById(
    request: Request,
    brand_id: UUID, service: AbstractBrandService = Depends(get_brand_service)
):
    return await service.get_by_id(brand_id)


@router.patch("/update/{brand_id}", response_model=BrandResponse)
@limiter.limit("30/minute")
async def update_brand(
    request: Request,
    brand_id: UUID,
    payload: UpdateBrandRequest,
    service: AbstractBrandService = Depends(get_brand_service),
) -> BrandResponse:
    brand = await service.update(
        brand_id,
        name=payload.name,
        description=payload.description,
        status=payload.status,
    )

    return BrandResponse(
        id=brand.id,
        name=brand.name,
        slug=brand.slug,
        description=brand.description,
        logo_media_url=brand.logo_media_url,
        status=brand.status.value,
        created_at=brand.created_at,
        updated_at=brand.updated_at,
    )


@router.delete(
    "/{brand_id}",
    response_model=DeleteResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
async def delete_brand(
    request: Request,
    brand_id: UUID,
    service: AbstractBrandService = Depends(get_brand_service),
) -> DeleteResponse:
    await service.delete(brand_id)

    return DeleteResponse(message="Brand deleted successfully")
