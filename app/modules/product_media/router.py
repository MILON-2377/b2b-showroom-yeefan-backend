from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.modules.product_media.dependencies import (
    get_product_media_service,
)
from app.modules.product_media.dto import UploadIntent
from app.modules.product_media.schema import (
    CreateUploadIntentRequest,
    FinalizeUploadRequest,
    ProductMediaResponse,
    UploadIntentResponse,
)
from app.modules.product_media.service import ProductMediaService

router = APIRouter(
    prefix="/products",
    tags=["product-media"],
)


@router.post(
    "/{product_id}/media/upload-intent",
    response_model=UploadIntentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_upload_intent(
    product_id: UUID,
    payload: CreateUploadIntentRequest,
    service: ProductMediaService = Depends(get_product_media_service),
) -> UploadIntent:
    return await service.create_upload_intent(
        storage_provider="local",
        product_id=product_id,
        media_type=payload.media_type,
        mime_type=payload.mime_type,
        original_filename=payload.original_filename,
        expires_in=payload.expires_in,
    )


@router.post(
    "/media/uploads/{upload_session_id}/finalize",
    response_model=ProductMediaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def finalize_upload(
    upload_session_id: UUID,
    payload: FinalizeUploadRequest,
    service: ProductMediaService = Depends(get_product_media_service),
) -> ProductMediaResponse:
    product_media = await service.finalize_upload(
        upload_session_id=upload_session_id,
        alt_text=payload.alt_text,
        sort_order=payload.sort_order,
        is_primary=payload.is_primary,
    )

    return ProductMediaResponse(
        id=product_media.id,
        product_id=product_media.product_id,
        media_asset_id=product_media.media_asset_id,
        alt_text=product_media.alt_text,
        sort_order=product_media.sort_order,
        is_primary=product_media.is_primary,
    )
