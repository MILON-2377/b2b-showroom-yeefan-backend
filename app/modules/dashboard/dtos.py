from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DashboardStatsDTO:
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


@dataclass(frozen=True, slots=True)
class DashboardInquiryDTO:
    id: UUID
    name: str
    company_name: str | None
    status: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class DashboardProductDTO:
    id: UUID
    name: str
    product_code: str
    status: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class DashboardReviewDTO:
    id: UUID
    name: str
    company_name: str | None
    rating: int
    status: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class DashboardDTO:
    stats: DashboardStatsDTO
    recent_inquiries: tuple[DashboardInquiryDTO, ...]
    recent_products: tuple[DashboardProductDTO, ...]
    pending_reviews: tuple[DashboardReviewDTO, ...]