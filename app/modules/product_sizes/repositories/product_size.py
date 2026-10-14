from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product_size import (
    AbstractProductSizeRepository,
)
from app.modules.product_sizes.models.product_size import ProductSize


class ProductSizeRepository(AbstractProductSizeRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create_many(
        self,
        sizes: list[ProductSize],
    ) -> list[ProductSize]:
        self.session.add_all(sizes)
        return sizes

    async def create(
        self,
        size: ProductSize,
    ) -> ProductSize:

        self.session.add(size)

        await self.session.flush()
        await self.session.refresh(size)

        return size

    async def get_by_id(
        self,
        size_id: UUID,
    ) -> ProductSize | None:

        result = await self.session.execute(
            select(ProductSize).where(
                ProductSize.id == size_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> list[ProductSize]:

        result = await self.session.execute(
            select(ProductSize)
            .where(
                ProductSize.product_id == product_id,
            )
            .order_by(ProductSize.sort_order, ProductSize.name)
        )

        return list(result.scalars().all())

    async def update(
        self,
        size: ProductSize,
    ) -> ProductSize:

        await self.session.flush()
        await self.session.refresh(size)

        return size

    async def update_many(
        self,
        sizes: list[ProductSize],
    ) -> list[ProductSize]:
        await self.session.flush()

        return sizes

    async def delete_many(
        self,
        sizes: list[ProductSize],
    ) -> None:

        await self.session.delete_all(sizes)

        await self.session.flush()

    async def delete(
        self,
        size: ProductSize,
    ) -> None:

        await self.session.delete(size)
        await self.session.flush()
