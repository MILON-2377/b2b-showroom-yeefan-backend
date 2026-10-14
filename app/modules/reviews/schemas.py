from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.reviews.model import ReviewStatus


class CreateReviewRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)
    job_title: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, max_length=100)
    rating: int = Field(ge=1, le=5)
    message: str = Field(min_length=1, max_length=5000)
    product_id: UUID | None = None
    avatar_media_id: UUID | None = None


class UpdateReviewRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)
    job_title: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, max_length=100)
    rating: int | None = Field(default=None, ge=1, le=5)
    message: str | None = Field(
        default=None,
        min_length=1,
        max_length=5000,
    )
    product_id: UUID | None = None
    avatar_media_id: UUID | None = None


class UpdateReviewStatusRequest(BaseModel):
    status: ReviewStatus


class UpdateReviewNotesRequest(BaseModel):
    internal_notes: str | None = Field(
        default=None,
        max_length=5000,
    )


class ReviewProductResponse(BaseModel):
    id: UUID
    name: str
    slug: str


class ReviewAvatarResponse(BaseModel):
    id: UUID
    url: str


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    company_name: str | None
    job_title: str | None
    country: str | None
    rating: int
    message: str
    product: ReviewProductResponse | None
    avatar: ReviewAvatarResponse | None
    status: ReviewStatus
    internal_notes: str | None

    @classmethod
    def from_dto(cls, dto) -> "ReviewResponse":
        return cls(
            id=dto.id,
            name=dto.name,
            company_name=dto.company_name,
            job_title=dto.job_title,
            country=dto.country,
            rating=dto.rating,
            message=dto.message,
            product=(
                ReviewProductResponse(
                    id=dto.product_id,
                    name=dto.product_name,
                    slug=dto.product_slug,
                )
                if dto.product_id is not None
                and dto.product_name is not None
                and dto.product_slug is not None
                else None
            ),
            avatar=(
                ReviewAvatarResponse(
                    id=dto.avatar_media_id,
                    url=dto.avatar_url,
                )
                if dto.avatar_media_id is not None and dto.avatar_url is not None
                else None
            ),
            status=dto.status,
            internal_notes=dto.internal_notes,
        )


class ReviewListResponse(BaseModel):
    items: list[ReviewResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class PublicReviewResponse(BaseModel):
    id: UUID
    name: str
    company_name: str | None
    job_title: str | None
    country: str | None
    rating: int
    message: str
    product: ReviewProductResponse | None
    avatar: ReviewAvatarResponse | None

    @classmethod
    def from_dto(cls, dto) -> "PublicReviewResponse":
        return cls(
            id=dto.id,
            name=dto.name,
            company_name=dto.company_name,
            job_title=dto.job_title,
            country=dto.country,
            rating=dto.rating,
            message=dto.message,
            product=(
                ReviewProductResponse(
                    id=dto.product_id,
                    name=dto.product_name,
                    slug=dto.product_slug,
                )
                if dto.product_id is not None
                and dto.product_name is not None
                and dto.product_slug is not None
                else None
            ),
            avatar=(
                ReviewAvatarResponse(
                    id=dto.avatar_media_id,
                    url=dto.avatar_url,
                )
                if dto.avatar_media_id is not None and dto.avatar_url is not None
                else None
            ),
        )


class PublicReviewListResponse(BaseModel):
    items: list[PublicReviewResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
