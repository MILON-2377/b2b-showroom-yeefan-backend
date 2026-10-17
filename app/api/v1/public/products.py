import logging
from math import ceil
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from app.core.contracts.services.product import AbstractProductService
from app.core.security.rate_limiter import limiter
from app.modules.products.dependencies import get_product_service
from app.modules.products.schemas import (
    ProductDetailQueryResponse,
    PublicFeaturedProductListResponse,
    PublicFeaturedProductResponse,
    PublicProductListResponse,
    PublicProductQuery,
    PublicProductResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
)


@router.get(
    "",
    response_model=PublicProductListResponse,
)
@limiter.limit("120/minute")
async def list_public_products(
    request: Request,
    query: Annotated[PublicProductQuery, Query()],
    service: Annotated[
        AbstractProductService,
        Depends(get_product_service),
    ],
) -> PublicProductListResponse:

    result = await service.list_public(
        query=query.to_dto(),
    )

    return PublicProductListResponse(
        items=[
            PublicProductResponse.from_dto(
                product,
            )
            for product in result.items
        ],
        next_cursor=result.next_cursor,
        has_more=result.has_more,
    )


@router.get(
    "/featured",
    response_model=PublicFeaturedProductListResponse,
)
@limiter.limit("120/minute")
async def list_featured_products(
    request: Request,
    service: Annotated[AbstractProductService, Depends(get_product_service)],
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=8,
        ge=1,
        le=100,
    ),
) -> PublicFeaturedProductListResponse:
    result = await service.list_featured(
        page=page,
        page_size=page_size,
    )

    total_pages = ceil(result.total / page_size) if result.total else 0

    return PublicFeaturedProductListResponse(
        items=[PublicFeaturedProductResponse.from_dto(item) for item in result.items],
        total=result.total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{product_id}",
    response_model=ProductDetailQueryResponse,
)
@limiter.limit("120/minute")
async def get_public_product(
    request: Request,
    product_id: UUID,
    service: Annotated[
        AbstractProductService,
        Depends(get_product_service),
    ],
) -> ProductDetailQueryResponse:
    dto = await service.get_public_by_id(product_id)

    return ProductDetailQueryResponse.from_dto(dto)
