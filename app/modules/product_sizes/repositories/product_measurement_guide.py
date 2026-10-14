from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product_measurement_guide import (
    AbstractProductMeasurementGuideRepository,
)
from app.modules.product_sizes.models.product_measurement_guide import (
    ProductMeasurementGuide,
)


class ProductMeasurementGuideRepository(AbstractProductMeasurementGuideRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        guide: ProductMeasurementGuide,
    ) -> ProductMeasurementGuide:

        self.session.add(guide)

        await self.session.flush()
        await self.session.refresh(guide)

        return guide

    async def get_by_id(
        self,
        guide_id: UUID,
    ) -> ProductMeasurementGuide | None:

        result = await self.session.execute(
            select(ProductMeasurementGuide).where(
                ProductMeasurementGuide.id == guide_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> ProductMeasurementGuide | None:

        result = await self.session.execute(
            select(ProductMeasurementGuide).where(
                ProductMeasurementGuide.product_id == product_id,
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        guide: ProductMeasurementGuide,
    ) -> ProductMeasurementGuide:

        await self.session.flush()

        return guide

    async def delete(
        self,
        guide: ProductMeasurementGuide,
    ) -> None:

        await self.session.delete(guide)
        await self.session.flush()
