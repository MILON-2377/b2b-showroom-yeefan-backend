from decimal import Decimal
from uuid import UUID

from app.core.contracts.services.size_measurement import (
    AbstractSizeMeasurementService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_sizes.dtos.size_measurement import (
    CreateSizeMeasurementDTO,
    SizeMeasurementDTO,
)
from app.modules.product_sizes.exceptions import SizeMeasurementNotFoundError
from app.modules.product_sizes.models.size_measurement import SizeMeasurement


class SizeMeasurementService(AbstractSizeMeasurementService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self.uow = uow

    async def create(
        self,
        *,
        product_size_id: UUID,
        payload: CreateSizeMeasurementDTO,
    ) -> SizeMeasurementDTO:

        measurement = SizeMeasurement(
            product_size_id=product_size_id,
            bust=payload.bust,
            waist=payload.waist,
            hips=payload.hips,
            hollow_to_hem=payload.hollow_to_hem,
            unit=payload.unit,
        )

        measurement = await self.uow.size_measurements.create(measurement)

        return self._to_dto(measurement)

    async def get(
        self,
        *,
        measurement_id: UUID,
    ) -> SizeMeasurementDTO:

        measurement = await self.uow.size_measurements.get_by_id(measurement_id)

        if measurement is None:
            raise SizeMeasurementNotFoundError(measurement_id)

        return self._to_dto(measurement)

    async def get_by_product_size_id(
        self,
        *,
        product_size_id: UUID,
    ) -> SizeMeasurementDTO | None:

        measurement = await self.uow.size_measurements.get_by_product_size_id(
            product_size_id
        )

        if measurement is None:
            return None

        return self._to_dto(measurement)

    async def update(
        self,
        *,
        measurement_id: UUID,
        bust: Decimal | None = None,
        waist: Decimal | None = None,
        hips: Decimal | None = None,
        hollow_to_hem: Decimal | None = None,
        unit: str = "cm",
    ) -> SizeMeasurementDTO:

        measurement = await self.uow.size_measurements.get_by_id(measurement_id)

        if measurement is None:
            raise SizeMeasurementNotFoundError(measurement_id)

        measurement.bust = bust
        measurement.waist = waist
        measurement.hips = hips
        measurement.hollow_to_hem = hollow_to_hem
        measurement.unit = unit

        measurement = await self.uow.size_measurements.update(measurement)

        await self.uow.commit()
        await self.uow.refresh(measurement)

        return self._to_dto(measurement)

    async def delete(
        self,
        *,
        measurement_id: UUID,
    ) -> None:

        measurement = await self.uow.size_measurements.get_by_id(measurement_id)

        if measurement is None:
            raise SizeMeasurementNotFoundError(measurement_id)

        await self.uow.size_measurements.delete(measurement)

        await self.uow.commit()

    @staticmethod
    def _to_dto(
        measurement: SizeMeasurement,
    ) -> SizeMeasurementDTO:
        return SizeMeasurementDTO(
            id=measurement.id,
            product_size_id=measurement.product_size_id,
            bust=measurement.bust,
            waist=measurement.waist,
            hips=measurement.hips,
            hollow_to_hem=measurement.hollow_to_hem,
            unit=measurement.unit,
            created_at=measurement.created_at,
            updated_at=measurement.updated_at,
        )
