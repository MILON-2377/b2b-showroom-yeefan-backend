from uuid import UUID

from pydantic import BaseModel, Field


class CreateUploadIntentRequest(BaseModel):
    media_type: str
    mime_type: str
    original_filename: str | None = None
    expires_in: int = Field(default=900, ge=1, le=3600)


class UploadIntentResponse(BaseModel):
    media_asset_id: UUID
    upload_session_id: UUID
    storage_key: str
    upload_url: str


class FinalizeUploadRequest(BaseModel):
    alt_text: str | None = None
    sort_order: int = Field(default=0, ge=0)
    is_primary: bool = False


class ProductMediaResponse(BaseModel):
    id: UUID
    product_id: UUID
    media_asset_id: UUID
    alt_text: str | None
    sort_order: int
    is_primary: bool
