from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product_media import (
    AbstractProductMediaRepository,
)
from app.modules.product_media.model import ProductMedia


class ProductMediaRepository(AbstractProductMediaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        product_media: ProductMedia,
    ) -> ProductMedia:
        self.session.add(product_media)

        await self.session.flush()
        await self.session.refresh(product_media)

        return product_media

    async def create_many(
        self, product_media: list[ProductMedia]
    ) -> list[ProductMedia]:
        self.session.add_all(product_media)
        await self.session.flush()
        return product_media

    async def get_by_id(
        self,
        product_media_id: UUID,
    ) -> ProductMedia | None:
        result = await self.session.execute(
            select(ProductMedia).where(ProductMedia.id == product_media_id)
        )

        return result.scalar_one_or_none()

    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> list[ProductMedia]:
        result = await self.session.execute(
            select(ProductMedia)
            .where(ProductMedia.product_id == product_id)
            .order_by(
                ProductMedia.sort_order,
                ProductMedia.id,
            )
        )

        return list(result.scalars().all())

    async def update(
        self,
        product_media: ProductMedia,
    ) -> ProductMedia:
        await self.session.flush()
        await self.session.refresh(product_media)

        return product_media

    async def update_many(
        self,
        product_media: list[ProductMedia],
    ) -> list[ProductMedia]:
        await self.session.flush()
        return product_media

    async def delete(
        self,
        product_media: ProductMedia,
    ) -> None:
        await self.session.delete(product_media)
        await self.session.flush()

    async def delete_many(self, product_media: list[ProductMedia]) -> None:

        await self.session.delete_all(product_media)

        await self.session.flush()
