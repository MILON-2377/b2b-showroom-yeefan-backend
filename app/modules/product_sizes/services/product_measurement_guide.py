from uuid import UUID

from app.core.contracts.services.product_measurement_guide import (
    AbstractProductMeasurementGuideService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_sizes.dtos.product_measurement_guide import (
    CreateProductMeasurementGuideDTO,
    ProductMeasurementGuideDTO,
    UpdateProductMeasurementGuideDTO,
)
from app.modules.product_sizes.exceptions import (
    ProductMeasurementGuideNotFoundError,
    ProductMeasurementGuideNotFoundForProductError,
)
from app.modules.product_sizes.models.product_measurement_guide import (
    ProductMeasurementGuide,
)


class ProductMeasurementGuideService(AbstractProductMeasurementGuideService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self.uow = uow

    async def create(
        self,
        *,
        product_id: UUID,
        payload: CreateProductMeasurementGuideDTO,
    ) -> ProductMeasurementGuideDTO:

        guide = ProductMeasurementGuide(
            product_id=product_id,
            title=payload.title,
            description=payload.description,
            measurement_unit=payload.measurement_unit,
            notes=payload.notes,
        )

        guide = await self.uow.product_measurement_guides.create(guide)

        return self._to_dto(guide)

    async def get_by_id(
        self,
        *,
        guide_id: UUID,
    ) -> ProductMeasurementGuideDTO:

        guide = await self.uow.product_measurement_guides.get_by_id(guide_id)

        if guide is None:
            raise ProductMeasurementGuideNotFoundError(guide_id)

        return self._to_dto(guide)

    async def get_by_product_id(
        self,
        *,
        product_id: UUID,
    ) -> ProductMeasurementGuideDTO:

        guide = await self.uow.product_measurement_guides.get_by_product_id(product_id)

        if guide is None:
            raise ProductMeasurementGuideNotFoundForProductError(product_id)

        return self._to_dto(guide)

    async def update(
        self,
        *,
        product_id: UUID,
        payload: UpdateProductMeasurementGuideDTO,
    ) -> ProductMeasurementGuideDTO:
        guide = await self.uow.product_measurement_guides.get_by_product_id(
            product_id=product_id,
        )

        if guide is None:
            guide = ProductMeasurementGuide(
                product_id=product_id,
                title=payload.title,
                description=payload.description,
                measurement_unit=payload.measurement_unit,
                notes=payload.notes,
            )

            await self.uow.product_measurement_guides.create(guide)

            return self._to_dto(guide)

        guide.title = payload.title
        guide.description = payload.description
        guide.measurement_unit = payload.measurement_unit
        guide.notes = payload.notes

        await self.uow.product_measurement_guides.update(guide)

        return self._to_dto(guide)

    async def delete(
        self,
        *,
        guide_id: UUID,
    ) -> None:

        guide = await self.uow.product_measurement_guides.get_by_id(guide_id)

        if guide is None:
            raise ProductMeasurementGuideNotFoundError(guide_id)

        await self.uow.product_measurement_guides.delete(guide)

        await self.uow.commit()

    @staticmethod
    def _to_dto(
        guide: ProductMeasurementGuide,
    ) -> ProductMeasurementGuideDTO:
        return ProductMeasurementGuideDTO(
            id=guide.id,
            product_id=guide.product_id,
            title=guide.title,
            description=guide.description,
            measurement_unit=guide.measurement_unit,
            notes=guide.notes,
            created_at=guide.created_at,
            updated_at=guide.updated_at,
        )
