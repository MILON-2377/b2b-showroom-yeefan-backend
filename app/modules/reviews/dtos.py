from dataclasses import dataclass
from uuid import UUID

from app.modules.reviews.model import ReviewStatus


@dataclass(frozen=True)
class CreateReviewDTO:
    name: str
    company_name: str | None
    job_title: str | None
    country: str | None
    rating: int
    message: str
    product_id: UUID | None
    avatar_media_id: UUID | None


@dataclass(frozen=True)
class UpdateReviewDTO:
    name: str | None = None
    company_name: str | None = None
    job_title: str | None = None
    country: str | None = None
    rating: int | None = None
    message: str | None = None
    product_id: UUID | None = None
    avatar_media_id: UUID | None = None


@dataclass(frozen=True)
class UpdateReviewStatusDTO:
    status: ReviewStatus


@dataclass(frozen=True)
class UpdateReviewNotesDTO:
    internal_notes: str | None


@dataclass(frozen=True)
class ReviewDTO:
    id: UUID
    name: str
    company_name: str | None
    job_title: str | None
    country: str | None
    rating: int
    message: str
    product_id: UUID | None
    product_name: str | None
    product_slug: str | None
    avatar_media_id: UUID | None
    avatar_url: str | None
    status: ReviewStatus
    internal_notes: str | None


@dataclass(frozen=True)
class ReviewListDTO:
    items: tuple[ReviewDTO, ...]
    total: int


@dataclass(frozen=True)
class PublicReviewDTO:
    id: UUID
    name: str
    company_name: str | None
    job_title: str | None
    country: str | None
    rating: int
    message: str
    product_id: UUID | None
    product_name: str | None
    product_slug: str | None
    avatar_media_id: UUID | None
    avatar_url: str | None


@dataclass(frozen=True)
class PublicReviewListDTO:
    items: tuple[PublicReviewDTO, ...]
    total: int
