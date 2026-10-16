from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response, status

from app.core.contracts.services.collection import AbstractCollectionService
from app.core.errors.schemas import DeleteResponse
from app.core.models import RecordStatus
from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.core.security.rate_limiter import limiter
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.collections.dependencies import get_collection_service
from app.modules.collections.query import CollectionListQuery
from app.modules.collections.schemas import (
    AvailableCatalogCollectionsResponse,
    CollectionListResponse,
    CollectionResponse,
    CreateCollectionRequest,
    UpdateCollectionRequest,
)

router = APIRouter(
    prefix="/collections",
    tags=["admin-collections"],
)


def to_collection_response(collection) -> CollectionResponse:
    return CollectionResponse(
        id=collection.id,
        brand_id=collection.brand_id,
        name=collection.name,
        slug=collection.slug,
        description=collection.description,
        cover_media_url=collection.cover_media_url,
        status=collection.status.value,
        created_at=collection.created_at,
        updated_at=collection.updated_at,
    )


@router.post(
    "",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("60/minute")
async def create_collection(
    request: Request,
    payload: CreateCollectionRequest,
    service: Annotated[
        AbstractCollectionService,
        Depends(get_collection_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COLLECTION_MANAGE)),
    ],
) -> CollectionResponse:

    collection = await service.create(
        brand_id=payload.brand_id,
        name=payload.name,
        description=payload.description,
    )

    return to_collection_response(collection)


@router.get(
    "",
    response_model=CollectionListResponse,
)
@limiter.limit("120/minute")
async def list_collections(
    service: Annotated[
        AbstractCollectionService,
        Depends(get_collection_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COLLECTION_READ)),
    ],
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    brand_id: UUID | None = Query(default=None),
    search: str | None = Query(default=None, min_length=1),
    status: RecordStatus | None = Query(default=None),
) -> CollectionListResponse:

    query = CollectionListQuery(
        page=page,
        page_size=page_size,
        brand_id=brand_id,
        search=search,
        status=status,
    )

    result = await service.list(query)

    return CollectionListResponse(
        items=[to_collection_response(collection) for collection in result.items],
        total=result.total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/available-for-catalogs",
    response_model=AvailableCatalogCollectionsResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")
async def list_collections_available_for_catalogs(
    request: Request,
    service: Annotated[
        AbstractCollectionService,
        Depends(get_collection_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COLLECTION_READ)),
    ],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
) -> AvailableCatalogCollectionsResponse:

    result = await service.list_by_unused_catalogs(
        page=page,
        page_size=page_size,
        search=search,
    )

    return AvailableCatalogCollectionsResponse(
        items=[
            CollectionResponse(
                id=item.id,
                brand_id=item.brand_id,
                name=item.name,
                slug=item.slug,
                description=item.description,
                status=item.status,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in result.items
        ],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )


@router.get(
    "/{collection_id}",
    response_model=CollectionResponse,
)
@limiter.limit("120/minute")
async def get_collection(
    request: Request,
    collection_id: UUID,
    service: Annotated[
        AbstractCollectionService,
        Depends(get_collection_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COLLECTION_READ)),
    ],
) -> CollectionResponse:

    collection = await service.get_by_id(collection_id)

    return to_collection_response(collection)


@router.patch(
    "/{collection_id}",
    response_model=CollectionResponse,
)
@limiter.limit("30/minute")
async def update_collection(
    request: Request,
    collection_id: UUID,
    payload: UpdateCollectionRequest,
    service: Annotated[
        AbstractCollectionService,
        Depends(get_collection_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COLLECTION_MANAGE)),
    ],
) -> CollectionResponse:

    collection = await service.update(
        collection_id,
        name=payload.name,
        description=payload.description,
        status=payload.status,
    )

    return to_collection_response(collection)


@router.delete(
    "/{collection_id}",
    response_model=DeleteResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
async def delete_collection(
    request: Request,
    collection_id: UUID,
    service: Annotated[
        AbstractCollectionService,
        Depends(get_collection_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COLLECTION_MANAGE)),
    ],
) -> DeleteResponse:

    await service.delete(collection_id)

    return DeleteResponse(message="One Collection Item Deleted successfully")
