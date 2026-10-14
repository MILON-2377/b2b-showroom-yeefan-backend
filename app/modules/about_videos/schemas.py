from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.models import RecordStatus
from app.modules.about_videos.dtos import (
    CreateAboutVideoDTO,
    UpdateAboutVideoDTO,
)


class CreateAboutVideoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    media_asset_id: UUID
    sort_order: int = Field(default=0, ge=0)
    status: RecordStatus = RecordStatus.DRAFT

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty.")
        return value

    def to_dto(self) -> CreateAboutVideoDTO:
        return CreateAboutVideoDTO(
            title=self.title,
            description=self.description,
            media_asset_id=self.media_asset_id,
            sort_order=self.sort_order,
            status=self.status,
        )


class UpdateAboutVideoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    media_asset_id: UUID | None = None
    sort_order: int | None = Field(default=None, ge=0)
    status: RecordStatus | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty.")
        return value

    def to_dto(self) -> UpdateAboutVideoDTO:
        data = self.model_dump(exclude_unset=True)
        return UpdateAboutVideoDTO(**data)


class AboutVideoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    media_asset_id: UUID
    video_url: str
    sort_order: int
    status: RecordStatus
    created_at: datetime
    updated_at: datetime


class AboutVideoListResponse(BaseModel):
    items: list[AboutVideoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
