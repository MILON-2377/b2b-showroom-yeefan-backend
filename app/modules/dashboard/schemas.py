from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DashboardStatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    products_total: int
    products_by_status: dict[str, int]

    inquiries_total: int
    inquiries_by_status: dict[str, int]

    reviews_total: int
    reviews_by_status: dict[str, int]

    collections_total: int
    catalogs_total: int

    media_assets_total: int
    media_assets_by_status: dict[str, int]


class DashboardInquiryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    company_name: str | None
    status: str
    created_at: datetime


class DashboardProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    product_code: str
    status: str
    created_at: datetime


class DashboardReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    company_name: str | None
    rating: int
    status: str
    created_at: datetime


class DashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stats: DashboardStatsResponse
    recent_inquiries: list[DashboardInquiryResponse]
    recent_products: list[DashboardProductResponse]
    pending_reviews: list[DashboardReviewResponse]
