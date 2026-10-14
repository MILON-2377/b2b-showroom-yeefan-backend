from uuid import UUID

from app.core.contracts.services.product_customization import (
    AbstractProductCustomizationService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_customizations.dtos.product_customization import (
    CreateProductCustomizationDTO,
    ProductCustomizationDTO,
    UpdateProductCustomizationDTO,
)
from app.modules.product_customizations.exceptions import (
    ProductCustomizationNotFoundError,
    ProductCustomizationNotFoundForProductError,
)
from app.modules.product_customizations.models.product_customization import (
    ProductCustomization,
)


class ProductCustomizationService(AbstractProductCustomizationService):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    @staticmethod
    def _to_dto(
        customization: ProductCustomization,
    ) -> ProductCustomizationDTO:
        return ProductCustomizationDTO(
            id=customization.id,
            product_id=customization.product_id,
            is_customizable=customization.is_customizable,
            notes=customization.notes,
            created_at=customization.created_at,
            updated_at=customization.updated_at,
        )

    async def create(
        self,
        *,
        product_id: UUID,
        payload: CreateProductCustomizationDTO,
    ) -> ProductCustomizationDTO:

        customization = ProductCustomization(
            product_id=product_id,
            is_customizable=payload.is_customizable,
            notes=payload.notes,
        )

        customization = await self.uow.product_customizations.create(customization)

        return self._to_dto(customization)

    async def get_by_id(
        self,
        customization_id: UUID,
    ) -> ProductCustomizationDTO:
        customization = await self.uow.product_customizations.get_by_id(
            customization_id
        )

        if customization is None:
            raise ProductCustomizationNotFoundError(customization_id)

        return self._to_dto(customization)

    async def get_by_product_id(
        self,
        product_id: UUID,
    ) -> ProductCustomizationDTO:
        customization = await self.uow.product_customizations.get_by_product_id(
            product_id
        )

        if customization is None:
            raise ProductCustomizationNotFoundForProductError(product_id)

        return self._to_dto(customization)

    async def update(
        self,
        *,
        product_id: UUID,
        payload: UpdateProductCustomizationDTO,
    ) -> ProductCustomizationDTO:
        customization = await self.uow.product_customizations.get_by_product_id(
            product_id=product_id,
        )

        if customization is None:
            customization = ProductCustomization(
                product_id=product_id,
                is_customizable=payload.is_customizable,
                notes=payload.notes,
            )

            await self.uow.product_customizations.create(
                customization,
            )

            return self._to_dto(customization)

        customization.is_customizable = payload.is_customizable
        customization.notes = payload.notes

        await self.uow.product_customizations.update(
            customization,
        )

        return self._to_dto(customization)

    async def delete(
        self,
        customization_id: UUID,
    ) -> None:
        customization = await self.uow.product_customizations.get_by_id(
            customization_id
        )

        if customization is None:
            raise ProductCustomizationNotFoundError(customization_id)

        await self.uow.product_customizations.delete(customization)

        await self.uow.commit()
