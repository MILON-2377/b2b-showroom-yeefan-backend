from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product_color import (
    AbstractProductColorRepository,
)
from app.modules.product_colors.model import ProductColor


class ProductColorRepository(AbstractProductColorRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create_many(
        self,
        colors: list[ProductColor],
    ) -> list[ProductColor]:
        self.session.add_all(colors)
        await self.session.flush()
        return colors

    async def create(
        self,
        color: ProductColor,
    ) -> ProductColor:

        self.session.add(color)

        await self.session.flush()
        await self.session.refresh(color)

        return color

    async def get_by_id(
        self,
        color_id: UUID,
    ) -> ProductColor | None:

        result = await self.session.execute(
            select(ProductColor).where(
                ProductColor.id == color_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> list[ProductColor]:

        result = await self.session.execute(
            select(ProductColor)
            .where(
                ProductColor.product_id == product_id,
            )
            .order_by(
                ProductColor.sort_order,
                ProductColor.name,
            )
        )

        return list(result.scalars().all())

    async def update(
        self,
        color: ProductColor,
    ) -> ProductColor:

        await self.session.flush()
        await self.session.refresh(color)

        return color

    async def update_many(self, colors: list[ProductColor]) -> list[ProductColor]:
        await self.session.flush()
        return colors

    async def delete(
        self,
        color: ProductColor,
    ) -> None:

        await self.session.delete(color)
        await self.session.flush()

    async def delete_many(self, colors: list[ProductColor]) -> None:
        await self.session.delete_all(colors)

        await self.session.flush()
