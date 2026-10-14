from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_customizations.dtos.product_customization_option import (
    ProductCustomizationOptionDTO,
)
from app.modules.product_customizations.models.product_customization_option import (
    CustomizationOptionType,
)


class AbstractProductCustomizationOptionService(ABC):
    @abstractmethod
    async def create(
        self,
        *,
        customization_id: UUID,
        option_type: CustomizationOptionType,
        details: str | None = None,
        sort_order: int = 0,
    ) -> ProductCustomizationOptionDTO: ...

    @abstractmethod
    async def get(
        self,
        option_id: UUID,
    ) -> ProductCustomizationOptionDTO: ...

    @abstractmethod
    async def list_by_customization(
        self,
        customization_id: UUID,
    ) -> list[ProductCustomizationOptionDTO]: ...

    @abstractmethod
    async def update(
        self,
        option_id: UUID,
        *,
        option_type: CustomizationOptionType,
        details: str | None,
        sort_order: int,
    ) -> ProductCustomizationOptionDTO: ...

    @abstractmethod
    async def delete(
        self,
        option_id: UUID,
    ) -> None: ...
