from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product_customization import (
    AbstractProductCustomizationRepository,
)
from app.modules.product_customizations.models.product_customization import (
    ProductCustomization,
)


class ProductCustomizationRepository(AbstractProductCustomizationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        customization: ProductCustomization,
    ) -> ProductCustomization:
        self.session.add(customization)

        await self.session.flush()
        await self.session.refresh(customization)

        return customization

    async def get_by_id(
        self,
        customization_id: UUID,
    ) -> ProductCustomization | None:
        result = await self.session.execute(
            select(ProductCustomization).where(
                ProductCustomization.id == customization_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> ProductCustomization | None:
        result = await self.session.execute(
            select(ProductCustomization).where(
                ProductCustomization.product_id == product_id
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        customization: ProductCustomization,
    ) -> ProductCustomization:
        await self.session.flush()
        return customization

    async def delete(
        self,
        customization: ProductCustomization,
    ) -> None:
        await self.session.delete(customization)
        await self.session.flush()
