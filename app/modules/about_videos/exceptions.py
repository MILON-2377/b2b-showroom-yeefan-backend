from uuid import UUID

from app.core.errors.base import NotFoundError, ValidationError


class AboutVideoNotFoundError(NotFoundError):
    def __init__(self, video_id: UUID) -> None:
        super().__init__(
            message=f"About video '{video_id}' was not found.",
            code="ABOUT_VIDEO_NOT_FOUND",
            details={"video_id": str(video_id)},
        )


class AboutVideoMediaValidationError(ValidationError):
    def __init__(self, media_asset_id: UUID) -> None:
        super().__init__(
            message="The selected media asset must be a ready video with a valid URL.",
            code="ABOUT_VIDEO_MEDIA_INVALID",
            details={"media_asset_id": str(media_asset_id)},
        )