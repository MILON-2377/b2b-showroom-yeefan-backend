from uuid import UUID

from app.core.errors.base import ConflictError, NotFoundError, ValidationError
from app.modules.media.model import MediaType


class UploadSessionNotFoundError(NotFoundError):
    def __init__(self, upload_session_id: UUID) -> None:
        super().__init__(
            "Upload session not found",
            code="UPLOAD_SESSION_NOT_FOUND",
        )
        self.upload_session_id = upload_session_id


class UploadSessionInvalidStateError(ConflictError):
    def __init__(self, upload_session_id: UUID) -> None:
        super().__init__(
            "Upload session is not in a valid state for finalization",
            code="UPLOAD_SESSION_INVALID_STATE",
        )
        self.upload_session_id = upload_session_id


class UploadSessionExpiredError(ConflictError):
    def __init__(self, upload_session_id: UUID) -> None:
        super().__init__(
            "Upload session has expired",
            code="UPLOAD_SESSION_EXPIRED",
        )
        self.upload_session_id = upload_session_id


class MediaAssetNotFoundError(NotFoundError):
    def __init__(self, media_asset_id: UUID) -> None:
        super().__init__(
            "Media asset not found",
            code="MEDIA_ASSET_NOT_FOUND",
        )
        self.media_asset_id = media_asset_id


class MediaAssetVerificationError(ConflictError):
    def __init__(self, media_asset_id: UUID) -> None:
        super().__init__(
            "Uploaded media asset could not be verified",
            code="MEDIA_ASSET_VERIFICATION_FAILED",
        )
        self.media_asset_id = media_asset_id


class MediaAssetNotReadyError(ConflictError):
    def __init__(self, media_asset_id: UUID):
        super().__init__(
            code="MEDIA_ASSET_NOT_READY",
            message=f"Media asset '{media_asset_id}' is not ready",
        )


class UnsupportedMediaTypeError(ValidationError):
    def __init__(self, media_type: MediaType) -> None:
        super().__init__(
            message=f"Unsupported media type: '{media_type.value}'.",
            code="UNSUPPORTED_MEDIA_TYPE",
            details={
                "media_type": media_type.value,
            },
        )
