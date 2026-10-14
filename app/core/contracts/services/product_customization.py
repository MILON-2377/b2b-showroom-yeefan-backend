from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_customizations.dtos.product_customization import (
    CreateProductCustomizationDTO,
    ProductCustomizationDTO,
    UpdateProductCustomizationDTO,
)


class AbstractProductCustomizationService(ABC):
    @abstractmethod
    async def create(
        self,
        *,
        product_id: UUID,
        payload: CreateProductCustomizationDTO,
    ) -> ProductCustomizationDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        customization_id: UUID,
    ) -> ProductCustomizationDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> ProductCustomizationDTO:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        *,
        product_id: UUID,
        payload: UpdateProductCustomizationDTO,
    ) -> ProductCustomizationDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        customization_id: UUID,
    ) -> None:
        raise NotImplementedError
