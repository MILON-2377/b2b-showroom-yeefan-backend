from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status

from app.core.contracts.services.catalog import AbstractCatalogService
from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.core.security.rate_limiter import limiter
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.catalogs.dependencies import get_catalog_service
from app.modules.catalogs.dtos import AdminCatalogQueryDTO
from app.modules.catalogs.schemas import (
    AdminCatalogListResponse,
    AdminCatalogQueryParams,
    AdminCatalogResponse,
    CatalogDetailResponse,
    CatalogResponse,
    CreateCatalogRequest,
    UpdateCatalogRequest,
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
    service: Annotated[
        AbstractCatalogService,
        Depends(get_catalog_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATALOG_MANAGE)),
    ],
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
    params: Annotated[
        AdminCatalogQueryParams,
        Depends(),
    ],
    service: Annotated[
        AbstractCatalogService,
        Depends(get_catalog_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATALOG_READ)),
    ],
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


@router.get(
    "/{catalog_id}",
    response_model=CatalogDetailResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")
async def get_catalog_by_id(
    request: Request,
    catalog_id: UUID,
    service: Annotated[
        AbstractCatalogService,
        Depends(get_catalog_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATALOG_READ)),
    ],
) -> CatalogDetailResponse:
    dto = await service.get_by_id(catalog_id=catalog_id)

    return CatalogDetailResponse.model_validate(dto)


@router.patch(
    "/{catalog_id}",
    response_model=CatalogDetailResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")
async def update_catalog(
    request: Request,
    catalog_id: UUID,
    payload: UpdateCatalogRequest,
    service: Annotated[
        AbstractCatalogService,
        Depends(get_catalog_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATALOG_MANAGE)),
    ],
) -> CatalogDetailResponse:
    dto = await service.update(
        catalog_id=catalog_id,
        payload=payload.to_dto(),
    )

    return CatalogDetailResponse.model_validate(dto)


@router.delete(
    "/{catalog_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("60/minute")
async def delete_catalog(
    request: Request,
    catalog_id: UUID,
    service: Annotated[
        AbstractCatalogService,
        Depends(get_catalog_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.CATALOG_MANAGE)),
    ],
) -> Response:
    await service.delete(catalog_id=catalog_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
