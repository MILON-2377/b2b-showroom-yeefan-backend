from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product_detail import (
    AbstractProductDetailRepository,
)
from app.modules.product_details.model import ProductDetail


class ProductDetailRepository(AbstractProductDetailRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        detail: ProductDetail,
    ) -> ProductDetail:
        self.session.add(detail)

        await self.session.flush()
        await self.session.refresh(detail)

        return detail

    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> ProductDetail | None:
        result = await self.session.execute(
            select(ProductDetail).where(ProductDetail.product_id == product_id)
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        detail: ProductDetail,
    ) -> ProductDetail:
        await self.session.flush()
        await self.session.refresh(detail)

        return detail

    async def delete(
        self,
        detail: ProductDetail,
    ) -> None:
        await self.session.delete(detail)
        await self.session.flush()
