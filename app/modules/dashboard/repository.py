from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.dashboard import (
    AbstractDashboardRepository,
)
from app.modules.catalogs.model import Catalog
from app.modules.collections.model import Collection
from app.modules.inquiries.models.inquiry import Inquiry
from app.modules.media.model import MediaAsset
from app.modules.products.model import Product
from app.modules.reviews.model import Review, ReviewStatus


class DashboardRepository(AbstractDashboardRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_stats(self) -> dict[str, Any]:
        products_by_status = await self._count_by_status(
            Product,
            Product.status,
        )

        inquiries_by_status = await self._count_by_status(
            Inquiry,
            Inquiry.status,
        )

        reviews_by_status = await self._count_by_status(
            Review,
            Review.status,
        )

        media_assets_by_status = await self._count_by_status(
            MediaAsset,
            MediaAsset.status,
        )

        return {
            "products_total": sum(products_by_status.values()),
            "products_by_status": products_by_status,
            "inquiries_total": sum(inquiries_by_status.values()),
            "inquiries_by_status": inquiries_by_status,
            "reviews_total": sum(reviews_by_status.values()),
            "reviews_by_status": reviews_by_status,
            "collections_total": await self._count_all(Collection),
            "catalogs_total": await self._count_all(Catalog),
            "media_assets_total": sum(media_assets_by_status.values()),
            "media_assets_by_status": media_assets_by_status,
        }

    async def _count_by_status(
        self,
        model: type,
        status_column: Any,
    ) -> dict[str, int]:
        stmt = (
            select(status_column, func.count())
            .select_from(model)
            .group_by(status_column)
        )

        result = await self.session.execute(stmt)

        return {self._status_value(status): count for status, count in result.all()}

    async def _count_all(self, model: type) -> int:
        stmt = select(func.count()).select_from(model)

        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def list_recent_inquiries(
        self,
        *,
        limit: int,
    ) -> list[Inquiry]:
        stmt = select(Inquiry).order_by(Inquiry.created_at.desc()).limit(limit)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def list_recent_products(
        self,
        *,
        limit: int,
    ) -> list[Product]:
        stmt = select(Product).order_by(Product.created_at.desc()).limit(limit)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def list_pending_reviews(
        self,
        *,
        limit: int,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .where(Review.status == ReviewStatus.PENDING)
            .order_by(Review.created_at.desc())
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    @staticmethod
    def _status_value(status: object) -> str:
        return str(getattr(status, "value", status))
