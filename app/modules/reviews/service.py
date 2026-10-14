from uuid import UUID

from app.core.contracts.services.review import AbstractReviewService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.media.model import MediaAssetStatus
from app.modules.reviews.dtos import (
    CreateReviewDTO,
    PublicReviewDTO,
    PublicReviewListDTO,
    ReviewDTO,
    ReviewListDTO,
    UpdateReviewDTO,
    UpdateReviewNotesDTO,
    UpdateReviewStatusDTO,
)
from app.modules.reviews.exceptions import (
    ReviewAvatarNotFoundError,
    ReviewAvatarNotReadyError,
    ReviewNotFoundError,
    ReviewProductNotFoundError,
)
from app.modules.reviews.model import Review, ReviewStatus


class ReviewService(AbstractReviewService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self.uow = uow

    async def create(
        self,
        payload: CreateReviewDTO,
    ) -> ReviewDTO:
        if payload.product_id is not None:
            product = await self.uow.products.get_by_id(
                payload.product_id,
            )

            if product is None:
                raise ReviewProductNotFoundError(
                    str(payload.product_id),
                )

        if payload.avatar_media_id is not None:
            await self._validate_avatar(
                payload.avatar_media_id,
            )

        review = Review(
            name=payload.name,
            company_name=payload.company_name,
            job_title=payload.job_title,
            country=payload.country,
            rating=payload.rating,
            message=payload.message,
            product_id=payload.product_id,
            avatar_media_id=payload.avatar_media_id,
            status=ReviewStatus.PENDING,
        )

        review = await self.uow.reviews.create(review)

        await self.uow.commit()

        created_review = await self.uow.reviews.get_by_id(review.id)

        if created_review is None:
            raise ReviewNotFoundError(str(review.id))

        return self._to_dto(review)

    async def get_by_id(
        self,
        review_id: UUID,
    ) -> ReviewDTO:
        review = await self.uow.reviews.get_by_id(review_id)

        if review is None:
            raise ReviewNotFoundError(
                str(review_id),
            )

        return self._to_dto(review)

    async def list(
        self,
        *,
        status: ReviewStatus | None,
        page: int,
        page_size: int,
    ) -> ReviewListDTO:
        reviews, total = await self.uow.reviews.list(
            status=status,
            page=page,
            page_size=page_size,
        )

        return ReviewListDTO(
            items=tuple(self._to_dto(review) for review in reviews),
            total=total,
        )

    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
    ) -> PublicReviewListDTO:
        reviews, total = await self.uow.reviews.list_public(
            page=page,
            page_size=page_size,
        )

        return PublicReviewListDTO(
            items=tuple(self._to_public_dto(review) for review in reviews),
            total=total,
        )

    async def update(
        self,
        review_id: UUID,
        payload: UpdateReviewDTO,
    ) -> ReviewDTO:
        review = await self.uow.reviews.get_by_id(review_id)

        if review is None:
            raise ReviewNotFoundError(
                str(review_id),
            )

        if payload.product_id is not None:
            product = await self.uow.products.get_by_id(
                payload.product_id,
            )

            if product is None:
                raise ReviewProductNotFoundError(
                    str(payload.product_id),
                )

        if payload.avatar_media_id is not None:
            await self._validate_avatar(
                payload.avatar_media_id,
            )

        if payload.name is not None:
            review.name = payload.name

        if payload.company_name is not None:
            review.company_name = payload.company_name

        if payload.job_title is not None:
            review.job_title = payload.job_title

        if payload.country is not None:
            review.country = payload.country

        if payload.rating is not None:
            review.rating = payload.rating

        if payload.message is not None:
            review.message = payload.message

        if payload.product_id is not None:
            review.product_id = payload.product_id

        if payload.avatar_media_id is not None:
            review.avatar_media_id = payload.avatar_media_id

        review = await self.uow.reviews.update(review)

        await self.uow.commit()

        return self._to_dto(review)

    async def update_status(
        self,
        review_id: UUID,
        payload: UpdateReviewStatusDTO,
    ) -> ReviewDTO:
        review = await self.uow.reviews.get_by_id(review_id)

        if review is None:
            raise ReviewNotFoundError(
                str(review_id),
            )

        review.status = payload.status

        review = await self.uow.reviews.update(review)

        await self.uow.commit()

        return self._to_dto(review)

    async def update_notes(
        self,
        review_id: UUID,
        payload: UpdateReviewNotesDTO,
    ) -> ReviewDTO:
        review = await self.uow.reviews.get_by_id(review_id)

        if review is None:
            raise ReviewNotFoundError(
                str(review_id),
            )

        review.internal_notes = payload.internal_notes

        review = await self.uow.reviews.update(review)

        await self.uow.commit()

        return self._to_dto(review)

    async def delete(
        self,
        review_id: UUID,
    ) -> None:
        review = await self.uow.reviews.get_by_id(review_id)

        if review is None:
            raise ReviewNotFoundError(
                str(review_id),
            )

        await self.uow.reviews.delete(review)

        await self.uow.commit()

    async def _validate_avatar(
        self,
        media_id: UUID,
    ) -> None:
        media = await self.uow.media_assets.get_by_id(
            media_id,
        )

        if media is None:
            raise ReviewAvatarNotFoundError(
                str(media_id),
            )

        if media.status != MediaAssetStatus.READY:
            raise ReviewAvatarNotReadyError(
                str(media_id),
            )

    @staticmethod
    def _to_dto(
        review: Review,
    ) -> ReviewDTO:
        return ReviewDTO(
            id=review.id,
            name=review.name,
            company_name=review.company_name,
            job_title=review.job_title,
            country=review.country,
            rating=review.rating,
            message=review.message,
            product_id=review.product_id,
            product_name=(review.product.name if review.product is not None else None),
            product_slug=(review.product.slug if review.product is not None else None),
            avatar_media_id=review.avatar_media_id,
            avatar_url=(
                review.avatar_media.secure_url
                if review.avatar_media is not None
                else None
            ),
            status=review.status,
            internal_notes=review.internal_notes,
        )

    @staticmethod
    def _to_public_dto(
        review: Review,
    ) -> PublicReviewDTO:
        return PublicReviewDTO(
            id=review.id,
            name=review.name,
            company_name=review.company_name,
            job_title=review.job_title,
            country=review.country,
            rating=review.rating,
            message=review.message,
            product_id=review.product_id,
            product_name=(review.product.name if review.product is not None else None),
            product_slug=(review.product.slug if review.product is not None else None),
            avatar_media_id=review.avatar_media_id,
            avatar_url=(
                review.avatar_media.secure_url
                if review.avatar_media is not None
                else None
            ),
        )
