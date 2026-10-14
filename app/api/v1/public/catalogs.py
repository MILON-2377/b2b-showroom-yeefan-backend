from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.contracts.services.catalog import AbstractCatalogService
from app.core.security.rate_limiter import limiter
from app.modules.catalogs.dependencies import get_catalog_service
from app.modules.catalogs.dtos import PublicCatalogQueryDTO
from app.modules.catalogs.schemas import (
    PublicCatalogListResponse,
    PublicCatalogQueryParams,
    PublicCatalogResponse,
)

router = APIRouter(prefix="/catalogs")


@router.get(
    "",
    response_model=PublicCatalogListResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("120/minute")
async def list_public_catalogs(
    request: Request,
    params: Annotated[PublicCatalogQueryParams, Depends()],
    catalog_service: Annotated[
        AbstractCatalogService,
        Depends(get_catalog_service),
    ],
) -> PublicCatalogListResponse:
    result = await catalog_service.list_public(
        PublicCatalogQueryDTO(
            page=params.page,
            page_size=params.page_size,
            search=params.search.strip() if params.search else None,
            collection_id=params.collection_id,
            sort_order=params.sort_order,
        )
    )

    return PublicCatalogListResponse(
        items=[
            PublicCatalogResponse(
                id=item.id,
                collection_id=item.collection_id,
                title=item.title,
                description=item.description,
                catalog_url=item.catalog_url,
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
    "/collection/{collection_id}",
    response_model=PublicCatalogResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("120/minute")
async def get_public_catalog_by_collection(
    request: Request,
    collection_id: UUID,
    catalog_service: Annotated[
        AbstractCatalogService,
        Depends(get_catalog_service),
    ],
) -> PublicCatalogResponse:
    catalog = await catalog_service.get_public_by_collection_id(
        collection_id=collection_id,
    )

    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog not found",
        )

    return PublicCatalogResponse(
        id=catalog.id,
        collection_id=catalog.collection_id,
        title=catalog.title,
        description=catalog.description,
        catalog_url=catalog.catalog_url,
        created_at=catalog.created_at,
        updated_at=catalog.updated_at,
    )
