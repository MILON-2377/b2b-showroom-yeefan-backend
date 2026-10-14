from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.inquiry_product import (
    AbstractInquiryProductRepository,
)
from app.modules.inquiries.models.inquiry_product import InquiryProduct


class InquiryProductRepository(
    AbstractInquiryProductRepository,
):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(
        self,
        inquiry_products: list[InquiryProduct],
    ) -> list[InquiryProduct]:
        self.session.add_all(inquiry_products)

        await self.session.flush()

        return inquiry_products

    async def get_by_inquiry_id(
        self,
        inquiry_id: UUID,
    ) -> list[InquiryProduct]:
        result = await self.session.execute(
            select(InquiryProduct)
            .where(
                InquiryProduct.inquiry_id == inquiry_id,
            )
            .order_by(InquiryProduct.created_at.asc())
        )

        return list(result.scalars().all())
