from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from app.modules.product_sizes.dtos.size_measurement import (
    CreateSizeMeasurementDTO,
    SizeMeasurementDTO,
)


class AbstractSizeMeasurementService(ABC):
    @abstractmethod
    async def create(
        self,
        *,
        product_size_id: UUID,
        payload: CreateSizeMeasurementDTO,
    ) -> SizeMeasurementDTO: ...

    @abstractmethod
    async def get(
        self,
        *,
        measurement_id: UUID,
    ) -> SizeMeasurementDTO: ...

    @abstractmethod
    async def get_by_product_size_id(
        self,
        *,
        product_size_id: UUID,
    ) -> SizeMeasurementDTO | None: ...

    @abstractmethod
    async def update(
        self,
        *,
        measurement_id: UUID,
        bust: Decimal | None = None,
        waist: Decimal | None = None,
        hips: Decimal | None = None,
        hollow_to_hem: Decimal | None = None,
        unit: str = "cm",
    ) -> SizeMeasurementDTO: ...

    @abstractmethod
    async def delete(
        self,
        *,
        measurement_id: UUID,
    ) -> None: ...
