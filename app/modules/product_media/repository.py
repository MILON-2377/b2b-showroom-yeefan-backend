from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product_media import (
    AbstractProductMediaRepository,
)
from app.modules.product_media.model import ProductMedia


class ProductMediaRepository(AbstractProductMediaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        product_media_id: UUID,
    ) -> ProductMedia | None:
        statement = select(ProductMedia).where(ProductMedia.id == product_media_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def list_by_product(
        self,
        product_id: UUID,
    ) -> list[ProductMedia]:
        statement = (
            select(ProductMedia)
            .where(ProductMedia.product_id == product_id)
            .order_by(ProductMedia.sort_order, ProductMedia.created_at)
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def add(
        self,
        product_media: ProductMedia,
    ) -> ProductMedia:
        self.session.add(product_media)
        return product_media

    async def delete(
        self,
        product_media: ProductMedia,
    ) -> None:
        await self.session.delete(product_media)
