from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.size_measurement import (
    AbstractSizeMeasurementRepository,
)
from app.modules.product_sizes.models.size_measurement import SizeMeasurement


class SizeMeasurementRepository(AbstractSizeMeasurementRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        measurement: SizeMeasurement,
    ) -> SizeMeasurement:

        self.session.add(measurement)

        await self.session.flush()
        await self.session.refresh(measurement)

        return measurement

    async def get_by_id(
        self,
        measurement_id: UUID,
    ) -> SizeMeasurement | None:

        result = await self.session.execute(
            select(SizeMeasurement).where(SizeMeasurement.id == measurement_id)
        )

        return result.scalar_one_or_none()

    async def get_by_product_size_id(
        self,
        product_size_id: UUID,
    ) -> SizeMeasurement | None:

        result = await self.session.execute(
            select(SizeMeasurement).where(
                SizeMeasurement.product_size_id == product_size_id
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        measurement: SizeMeasurement,
    ) -> SizeMeasurement:

        await self.session.flush()
        await self.session.refresh(measurement)

        return measurement

    async def delete(
        self,
        measurement: SizeMeasurement,
    ) -> None:

        await self.session.delete(measurement)
        await self.session.flush()
