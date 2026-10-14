from uuid import UUID

from app.core.contracts.services.product_customization_option import (
    AbstractProductCustomizationOptionService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_customizations.dtos.product_customization_option import (
    ProductCustomizationOptionDTO,
)
from app.modules.product_customizations.exceptions import (
    ProductCustomizationOptionNotFoundError,
)
from app.modules.product_customizations.models.product_customization_option import (
    CustomizationOptionType,
    ProductCustomizationOption,
)


class ProductCustomizationOptionService(AbstractProductCustomizationOptionService):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    @staticmethod
    def _to_dto(
        option: ProductCustomizationOption,
    ) -> ProductCustomizationOptionDTO:
        return ProductCustomizationOptionDTO(
            id=option.id,
            customization_id=option.customization_id,
            option_type=option.option_type,
            details=option.details,
            sort_order=option.sort_order,
            created_at=option.created_at,
            updated_at=option.updated_at,
        )

    async def create(
        self,
        *,
        customization_id: UUID,
        option_type: CustomizationOptionType,
        details: str | None = None,
        sort_order: int = 0,
    ) -> ProductCustomizationOptionDTO:
        option = ProductCustomizationOption(
            customization_id=customization_id,
            option_type=option_type,
            details=details,
            sort_order=sort_order,
        )

        option = await self.uow.product_customization_options.create(option)

        return self._to_dto(option)

    async def get(
        self,
        option_id: UUID,
    ) -> ProductCustomizationOptionDTO:
        option = await self.uow.product_customization_options.get_by_id(option_id)

        if option is None:
            raise ProductCustomizationOptionNotFoundError(option_id)

        return self._to_dto(option)

    async def list_by_customization(
        self,
        customization_id: UUID,
    ) -> list[ProductCustomizationOptionDTO]:
        options = await self.uow.product_customization_options.get_by_customization_id(
            customization_id
        )

        return [self._to_dto(option) for option in options]

    async def update(
        self,
        option_id: UUID,
        *,
        option_type: CustomizationOptionType,
        details: str | None,
        sort_order: int,
    ) -> ProductCustomizationOptionDTO:
        option = await self.uow.product_customization_options.get_by_id(option_id)

        if option is None:
            raise ProductCustomizationOptionNotFoundError(option_id)

        option.option_type = option_type
        option.details = details
        option.sort_order = sort_order

        option = await self.uow.product_customization_options.update(option)

        await self.uow.commit()
        await self.uow.refresh(option)

        return self._to_dto(option)

    async def delete(
        self,
        option_id: UUID,
    ) -> None:
        option = await self.uow.product_customization_options.get_by_id(option_id)

        if option is None:
            raise ProductCustomizationOptionNotFoundError(option_id)

        await self.uow.product_customization_options.delete(option)

        await self.uow.commit()
