from fastapi import APIRouter, Depends, Request, status

from app.core.contracts.services.catalog import AbstractCatalogService
from app.core.security.rate_limiter import limiter
from app.modules.catalogs.dependencies import get_catalog_service
from app.modules.catalogs.dtos import AdminCatalogQueryDTO
from app.modules.catalogs.schemas import (
    AdminCatalogListResponse,
    AdminCatalogQueryParams,
    AdminCatalogResponse,
    CatalogResponse,
    CreateCatalogRequest,
)

router = APIRouter(
    prefix="/catalogs",
    tags=["admin-catalogs"],
)


@router.post(
    "",
    response_model=CatalogResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("60/minute")
async def create_catalog(
    request: Request,
    payload: CreateCatalogRequest,
    service: AbstractCatalogService = Depends(get_catalog_service),
) -> CatalogResponse:
    dto = await service.create(payload.to_dto())
    return CatalogResponse.model_validate(dto)


@router.get(
    "",
    response_model=AdminCatalogListResponse,
)
@limiter.limit("120/minute")
async def list_catalogs(
    request: Request,
    params: AdminCatalogQueryParams = Depends(),
    service: AbstractCatalogService = Depends(get_catalog_service),
) -> AdminCatalogListResponse:
    result = await service.list_admin(
        AdminCatalogQueryDTO(
            page=params.page,
            page_size=params.page_size,
            search=params.search,
            status=params.status,
            collection_id=params.collection_id,
            sort_order=params.sort_order,
        )
    )

    return AdminCatalogListResponse(
        items=[
            AdminCatalogResponse(
                id=item.id,
                collection_id=item.collection_id,
                pdf_media_asset_id=item.pdf_media_asset_id,
                cover_media_asset_id=item.cover_media_asset_id,
                title=item.title,
                description=item.description,
                pdf_url=item.pdf_url,
                status=item.status,
                cover_image_url=item.cover_image_url,
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
