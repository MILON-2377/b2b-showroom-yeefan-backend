from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.models import RecordStatus
from app.modules.catalogs.dtos import (
    CreateCatalogDTO,
    UpdateCatalogDTO,
)


class CreateCatalogRequest(BaseModel):
    collection_id: UUID
    pdf_media_asset_id: UUID
    cover_media_asset_id: UUID
    title: str = Field(
        min_length=1,
        max_length=255,
    )
    description: str | None = None

    def to_dto(self) -> CreateCatalogDTO:
        return CreateCatalogDTO(
            collection_id=self.collection_id,
            pdf_media_asset_id=self.pdf_media_asset_id,
            cover_media_asset_id=self.cover_media_asset_id,
            title=self.title,
            description=self.description,
        )


class UpdateCatalogRequest(BaseModel):
    pdf_media_asset_id: UUID | None = None
    cover_media_asset_id: UUID | None = None
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    status: RecordStatus | None = None
    description: str | None = None

    def to_dto(self) -> UpdateCatalogDTO:
        return UpdateCatalogDTO(
            pdf_media_asset_id=self.pdf_media_asset_id,
            cover_media_asset_id=self.cover_media_asset_id,
            title=self.title,
            status=self.status,
            description=self.description,
        )


class CatalogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    collection_id: UUID
    pdf_media_asset_id: UUID
    cover_media_asset_id: UUID
    title: str
    description: str | None
    status: RecordStatus
    created_at: datetime
    updated_at: datetime


class PublicCatalogQueryParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=12, ge=1, le=100)
    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    collection_id: UUID | None = None
    sort_order: Literal["asc", "desc"] = "desc"


class PublicCatalogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    collection_id: UUID
    title: str
    description: str | None
    catalog_url: str
    cover_image_url: str
    created_at: datetime
    updated_at: datetime


class PublicCatalogListResponse(BaseModel):
    items: list[PublicCatalogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AdminCatalogQueryParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=12, ge=1, le=100)
    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    collection_id: UUID | None = None
    status: RecordStatus | None = None
    sort_order: Literal["asc", "desc"] = "desc"


class AdminCatalogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    collection_id: UUID
    pdf_media_asset_id: UUID
    cover_media_asset_id: UUID
    title: str
    description: str | None
    status: RecordStatus
    pdf_url: str
    cover_image_url: str
    created_at: datetime
    updated_at: datetime


class AdminCatalogListResponse(BaseModel):
    items: list[AdminCatalogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int