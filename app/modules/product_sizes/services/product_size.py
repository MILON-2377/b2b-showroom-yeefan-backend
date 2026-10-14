from uuid import UUID

from app.core.contracts.services.product_size import (
    AbstractProductSizeService,
)
from app.core.contracts.services.size_measurement import AbstractSizeMeasurementService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_sizes.dtos.product_size import (
    CreateProductSizeWithMeasurementDTO,
    ProductSizeDTO,
    UpdateProductSizeDTO,
)
from app.modules.product_sizes.exceptions import ProductSizeNotFoundError
from app.modules.product_sizes.models.product_size import ProductSize


class ProductSizeService(AbstractProductSizeService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        size_measurement_service: AbstractSizeMeasurementService,
    ) -> None:
        self.uow = uow
        self.size_measurement_service = size_measurement_service

    async def create_many(
        self,
        *,
        product_id: UUID,
        payloads: tuple[CreateProductSizeWithMeasurementDTO, ...],
    ) -> list[ProductSizeDTO]:

        results = []

        for payload in payloads:
            product_size = ProductSize(
                product_id=product_id,
                name=payload.size.name,
                sort_order=payload.size.sort_order,
            )

            product_size = await self.uow.product_sizes.create(product_size)

            if payload.measurement is not None:
                await self.size_measurement_service.create(
                    product_size_id=product_size.id,
                    payload=payload.measurement,
                )

            results.append(self._to_dto(product_size))

        return results

    async def create(
        self,
        *,
        product_id: UUID,
        name: str,
        sort_order: int = 0,
    ) -> ProductSizeDTO:

        size = ProductSize(
            product_id=product_id,
            name=name,
            sort_order=sort_order,
        )

        size = await self.uow.product_sizes.create(size)

        return self._to_dto(size)

    async def get(
        self,
        *,
        size_id: UUID,
    ) -> ProductSizeDTO:

        size = await self.uow.product_sizes.get_by_id(size_id)

        if size is None:
            raise ProductSizeNotFoundError(size_id)

        return self._to_dto(size)

    async def list_by_product(
        self,
        *,
        product_id: UUID,
    ) -> list[ProductSizeDTO]:

        sizes = await self.uow.product_sizes.get_by_product_id(product_id)

        return [self._to_dto(size) for size in sizes]

    async def update(
        self,
        *,
        size_id: UUID,
        name: str,
        sort_order: int,
    ) -> ProductSizeDTO:

        size = await self.uow.product_sizes.get_by_id(size_id)

        if size is None:
            raise ProductSizeNotFoundError(size_id)

        size.name = name
        size.sort_order = sort_order

        size = await self.uow.product_sizes.update(size)

        await self.uow.commit()
        await self.uow.refresh(size)

        return self._to_dto(size)

    async def update_many(
        self,
        *,
        product_id: UUID,
        payloads: tuple[UpdateProductSizeDTO, ...],
    ) -> list[ProductSizeDTO]:
        payloads_list = list(payloads)

        existing_sizes = await self.uow.product_sizes.get_by_product_id(
            product_id=product_id,
        )

        existing_by_id = {size.id: size for size in existing_sizes}

        submitted_ids = {
            payload.id for payload in payloads_list if payload.id is not None
        }

        for size_id in submitted_ids:
            if size_id not in existing_by_id:
                raise ProductSizeNotFoundError(size_id)

        removed_sizes = [
            size for size in existing_sizes if size.id not in submitted_ids
        ]

        if removed_sizes:
            await self.uow.product_sizes.delete_many(
                removed_sizes,
            )

        new_sizes: list[ProductSize] = []
        updated_sizes: list[ProductSize] = []

        for payload in payloads_list:
            if payload.id is None:
                new_sizes.append(
                    ProductSize(
                        product_id=product_id,
                        name=payload.name,
                        sort_order=payload.sort_order,
                    )
                )
                continue

            size = existing_by_id[payload.id]

            size.name = payload.name
            size.sort_order = payload.sort_order

            updated_sizes.append(size)

        if new_sizes:
            await self.uow.product_sizes.create_many(
                new_sizes,
            )

        if updated_sizes:
            await self.uow.product_sizes.update_many(
                updated_sizes,
            )

        return [self._to_dto(size) for size in [*updated_sizes, *new_sizes]]

    async def delete(
        self,
        *,
        size_id: UUID,
    ) -> None:

        size = await self.uow.product_sizes.get_by_id(size_id)

        if size is None:
            raise ProductSizeNotFoundError(size_id)

        await self.uow.product_sizes.delete(size)

        await self.uow.commit()

    @staticmethod
    def _to_dto(
        size: ProductSize,
    ) -> ProductSizeDTO:
        return ProductSizeDTO(
            id=size.id,
            product_id=size.product_id,
            name=size.name,
            sort_order=size.sort_order,
            created_at=size.created_at,
            updated_at=size.updated_at,
        )
