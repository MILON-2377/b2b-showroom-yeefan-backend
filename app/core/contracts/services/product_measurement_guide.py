from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_sizes.dtos.product_measurement_guide import (
    CreateProductMeasurementGuideDTO,
    ProductMeasurementGuideDTO,
    UpdateProductMeasurementGuideDTO,
)


class AbstractProductMeasurementGuideService(ABC):
    @abstractmethod
    async def create(
        self,
        *,
        product_id: UUID,
        payload: CreateProductMeasurementGuideDTO,
    ) -> ProductMeasurementGuideDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        *,
        guide_id: UUID,
    ) -> ProductMeasurementGuideDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_product_id(
        self,
        *,
        product_id: UUID,
    ) -> ProductMeasurementGuideDTO:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        *,
        product_id: UUID,
        payload: UpdateProductMeasurementGuideDTO,
    ) -> ProductMeasurementGuideDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        *,
        guide_id: UUID,
    ) -> None:
        raise NotImplementedError
