from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_sizes.models.product_measurement_guide import (
    ProductMeasurementGuide,
)


class AbstractProductMeasurementGuideRepository(ABC):
    @abstractmethod
    async def create(
        self,
        guide: ProductMeasurementGuide,
    ) -> ProductMeasurementGuide:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        guide_id: UUID,
    ) -> ProductMeasurementGuide | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> ProductMeasurementGuide | None:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        guide: ProductMeasurementGuide,
    ) -> ProductMeasurementGuide:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        guide: ProductMeasurementGuide,
    ) -> None:
        raise NotImplementedError
