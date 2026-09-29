from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product import (
    AbstractProductRepository,
)
from app.core.models import RecordStatus
from app.modules.products.model import Product


class ProductRepository(AbstractProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        product_id: UUID,
    ) -> Product | None:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        brand_id: UUID,
        slug: str,
    ) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.brand_id == brand_id,
                Product.slug == slug,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_product_code(
        self,
        brand_id: UUID,
        product_code: str,
    ) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.brand_id == brand_id,
                Product.product_code == product_code,
            )
        )

        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        brand_id: UUID | None = None,
        collection_id: UUID | None = None,
        category_id: UUID | None = None,
        status: RecordStatus | None = None,
    ) -> list[Product]:
        statement = select(Product).order_by(Product.name)

        if brand_id is not None:
            statement = statement.where(Product.brand_id == brand_id)

        if collection_id is not None:
            statement = statement.where(Product.collection_id == collection_id)

        if category_id is not None:
            statement = statement.where(Product.category_id == category_id)

        if status is not None:
            statement = statement.where(Product.status == status)

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def exists_by_slug(
        self,
        brand_id: UUID,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool:
        statement = select(Product.id).where(
            Product.brand_id == brand_id,
            Product.slug == slug,
        )

        if exclude_id is not None:
            statement = statement.where(Product.id != exclude_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def exists_by_product_code(
        self,
        brand_id: UUID,
        product_code: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool:
        statement = select(Product.id).where(
            Product.brand_id == brand_id,
            Product.product_code == product_code,
        )

        if exclude_id is not None:
            statement = statement.where(Product.id != exclude_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def add(
        self,
        product: Product,
    ) -> Product:
        self.session.add(product)
        return product

    async def delete(
        self,
        product: Product,
    ) -> None:
        await self.session.delete(product)
