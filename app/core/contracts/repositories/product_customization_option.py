from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_customizations.models.product_customization_option import (
    ProductCustomizationOption,
)


class AbstractProductCustomizationOptionRepository(ABC):
    @abstractmethod
    async def create(
        self,
        option: ProductCustomizationOption,
    ) -> ProductCustomizationOption: ...

    @abstractmethod
    async def get_by_id(
        self,
        option_id: UUID,
    ) -> ProductCustomizationOption | None: ...

    @abstractmethod
    async def get_by_customization_id(
        self,
        customization_id: UUID,
    ) -> list[ProductCustomizationOption]: ...

    @abstractmethod
    async def update(
        self,
        option: ProductCustomizationOption,
    ) -> ProductCustomizationOption: ...

    @abstractmethod
    async def delete(
        self,
        option: ProductCustomizationOption,
    ) -> None: ...
