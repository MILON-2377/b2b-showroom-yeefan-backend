from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from app.core.contracts.services.product import AbstractProductService
from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.core.security.rate_limiter import limiter
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.products.dependencies import get_product_service
from app.modules.products.dtos import ProductQueryDTO
from app.modules.products.schemas import (
    CreateProductRequest,
    ProductDetailQueryResponse,
    ProductListResponse,
    ProductQueryParams,
    ProductResponse,
    UpdateProductRequest,
)
from app.modules.products.service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("60/minute")
async def create_product(
    request: Request,
    payload: CreateProductRequest,
    product_service: Annotated[
        AbstractProductService,
        Depends(get_product_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.PRODUCT_MANAGE)),
    ],
) -> ProductResponse:
    dto = await product_service.create(
        payload=product_service._to_create_product_dto(payload),
    )

    return ProductResponse.from_dto(dto)


@router.get(
    "",
    response_model=ProductListResponse,
)
@limiter.limit("120/minute")
async def list_products(
    request: Request,
    params: Annotated[
        ProductQueryParams,
        Depends(),
    ],
    service: Annotated[
        AbstractProductService,
        Depends(get_product_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.PRODUCT_READ)),
    ],
) -> ProductListResponse:

    query = ProductQueryDTO(
        search=params.search,
        status=params.status,
        brand_id=params.brand_id,
        collection_id=params.collection_id,
        category_id=params.category_id,
        page=params.page,
        page_size=params.page_size,
        sort_by=params.sort_by.value,
        sort_order=params.sort_order.value,
    )

    result = await service.list(
        query=query,
    )

    return ProductListResponse.from_dto(result)


@router.get(
    "/{product_id}",
    response_model=ProductDetailQueryResponse,
)
@limiter.limit("120/minute")
async def get_product(
    request: Request,
    product_id: UUID,
    service: Annotated[
        AbstractProductService,
        Depends(get_product_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.PRODUCT_READ)),
    ],
) -> ProductDetailQueryResponse:
    dto = await service.get_by_id(product_id)

    return ProductDetailQueryResponse.from_dto(dto)


@router.patch(
    "/{product_id}",
    response_model=ProductDetailQueryResponse,
)
@limiter.limit("60/minute")
async def update_product(
    request: Request,
    product_id: UUID,
    payload: UpdateProductRequest,
    service: Annotated[
        AbstractProductService,
        Depends(
            get_product_service,
        ),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.PRODUCT_MANAGE)),
    ],
) -> ProductDetailQueryResponse:
    dto = await service.update(
        product_id=product_id,
        payload=ProductService._to_update_product_dto(payload),
    )

    return ProductDetailQueryResponse.from_dto(dto)
