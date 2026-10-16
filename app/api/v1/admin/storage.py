from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.core.security.rate_limiter import limiter
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.media.dependencies import get_media_upload_service
from app.modules.media.dtos import CreateUploadIntentDTO, UploadIntent
from app.modules.media.schemas import (
    FinalizeUploadResponse,
    UploadIntentRequest,
    UploadIntentResponse,
)

router = APIRouter(
    prefix="/storage",
    tags=["Storage"],
)


@router.post(
    "/upload-intents",
    response_model=UploadIntentResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("60/minute")
async def create_upload_intent(
    request: Request,
    payload: UploadIntentRequest,
    service: Annotated[
        AbstractMediaUploadService,
        Depends(get_media_upload_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.MEDIA_UPLOAD)),
    ],
) -> UploadIntent:
    return await service.create_upload_intent(
        CreateUploadIntentDTO(
            storage_provider=payload.storage_provider,
            entity_id=payload.entity_id,
            namespace=payload.namespace,
            media_type=payload.media_type,
            mime_type=payload.mime_type,
            original_filename=payload.original_filename,
            expires_in=payload.expires_in,
        )
    )


@router.post(
    "/upload-sessions/{upload_session_id}/finalize",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")
async def finalize_upload(
    request: Request,
    upload_session_id: UUID,
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.MEDIA_UPLOAD)),
    ],
    service: Annotated[
        AbstractMediaUploadService,
        Depends(get_media_upload_service),
    ],
) -> FinalizeUploadResponse:
    media_asset = await service.finalize_upload(
        upload_session_id=upload_session_id,
    )

    return FinalizeUploadResponse(
        media_asset_id=media_asset.id,
        status=media_asset.status.value,
    )
