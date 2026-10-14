from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.media.model import MediaType


class UploadIntentRequest(BaseModel):
    storage_provider: str = Field(default="cloudinary")
    entity_id: UUID
    namespace: str
    media_type: MediaType
    mime_type: str
    original_filename: str | None = None
    expires_in: int = Field(default=900, ge=60, le=3600)


class FinalizeUploadResponse(BaseModel):
    media_asset_id: UUID
    status: str


class UploadIntentResponse(BaseModel):
    media_asset_id: UUID
    upload_session_id: UUID
    storage_key: str
    upload_url: str
    upload_params: dict[str, str]
