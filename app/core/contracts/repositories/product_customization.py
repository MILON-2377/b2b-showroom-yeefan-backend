from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_customizations.models.product_customization import (
    ProductCustomization,
)


class AbstractProductCustomizationRepository(ABC):
    @abstractmethod
    async def create(
        self,
        customization: ProductCustomization,
    ) -> ProductCustomization:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        customization_id: UUID,
    ) -> ProductCustomization | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> ProductCustomization | None:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        customization: ProductCustomization,
    ) -> ProductCustomization:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        customization: ProductCustomization,
    ) -> None:
        raise NotImplementedError
