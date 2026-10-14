from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_sizes.models.size_measurement import SizeMeasurement


class AbstractSizeMeasurementRepository(ABC):
    @abstractmethod
    async def create(
        self,
        measurement: SizeMeasurement,
    ) -> SizeMeasurement: ...

    @abstractmethod
    async def get_by_id(
        self,
        measurement_id: UUID,
    ) -> SizeMeasurement | None: ...

    @abstractmethod
    async def get_by_product_size_id(
        self,
        product_size_id: UUID,
    ) -> SizeMeasurement | None: ...

    @abstractmethod
    async def update(
        self,
        measurement: SizeMeasurement,
    ) -> SizeMeasurement: ...

    @abstractmethod
    async def delete(
        self,
        measurement: SizeMeasurement,
    ) -> None: ...
