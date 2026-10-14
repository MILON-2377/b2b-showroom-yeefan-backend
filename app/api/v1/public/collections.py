from fastapi import APIRouter, Depends, Request

from app.core.contracts.services.collection import (
    AbstractCollectionService,
)
from app.modules.collections.dependencies import get_collection_service
from app.modules.collections.dtos import PublicCollectionQueryDTO
from app.modules.collections.schemas import (
    PublicCollectionListResponse,
    PublicCollectionQueryParams,
    PublicCollectionResponse,
)

router = APIRouter(prefix="/collections")


@router.get(
    "",
    response_model=PublicCollectionListResponse,
)
async def list_public_collections(
    request: Request,
    params: PublicCollectionQueryParams = Depends(),
    service: AbstractCollectionService = Depends(get_collection_service),
) -> PublicCollectionListResponse:
    result = await service.list_public(
        PublicCollectionQueryDTO(
            page=params.page,
            page_size=params.page_size,
            search=params.search,
        )
    )

    return PublicCollectionListResponse(
        items=[
            PublicCollectionResponse(
                id=item.id,
                brand_id=item.brand_id,
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
