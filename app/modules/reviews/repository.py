from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.contracts.repositories.review import (
    AbstractReviewRepository,
)
from app.modules.reviews.model import Review, ReviewStatus


class ReviewRepository(
    AbstractReviewRepository,
):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        review: Review,
    ) -> Review:
        self.session.add(review)

        await self.session.flush()
        return review

    async def get_by_id(
        self,
        review_id: UUID,
    ) -> Review | None:
        stmt = (
            select(Review)
            .options(
                selectinload(Review.avatar_media),
                selectinload(Review.product),
            )
            .where(Review.id == review_id)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        status: ReviewStatus | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Review], int]:

        conditions = []

        if status is not None:
            conditions.append(Review.status == status)

        count_stmt = select(func.count(Review.id)).where(*conditions)

        total = await self.session.scalar(count_stmt)
        total = total or 0

        offset = (page - 1) * page_size

        stmt = (
            select(Review)
            .options(
                selectinload(Review.avatar_media),
                selectinload(Review.product),
            )
            .where(*conditions)
            .order_by(Review.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all()), total

    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[Review], int]:

        conditions = [
            Review.status == ReviewStatus.APPROVED,
        ]

        count_stmt = select(func.count(Review.id)).where(*conditions)

        total = await self.session.scalar(count_stmt)
        total = total or 0

        offset = (page - 1) * page_size

        stmt = (
            select(Review)
            .options(
                selectinload(Review.avatar_media),
                selectinload(Review.product),
            )
            .where(*conditions)
            .order_by(Review.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all()), total

    async def update(
        self,
        review: Review,
    ) -> Review:
        await self.session.flush()

        return review

    async def delete(
        self,
        review: Review,
    ) -> None:
        await self.session.delete(review)

        await self.session.flush()
