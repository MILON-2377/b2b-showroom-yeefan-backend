from uuid import UUID

from app.core.contracts.services.product_color import (
    AbstractProductColorService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_colors.dtos import (
    CreateProductColorDTO,
    ProductColorDTO,
    UpdateProductColorDTO,
)
from app.modules.product_colors.exceptions import ProductColorNotFoundError
from app.modules.product_colors.model import ProductColor


class ProductColorService(AbstractProductColorService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self.uow = uow

    async def create_many(
        self,
        *,
        product_id: UUID,
        payloads: list[CreateProductColorDTO],
    ) -> list[ProductColorDTO]:
        if not payloads:
            return []

        colors = [
            ProductColor(
                product_id=product_id,
                name=payload.name,
                sort_order=payload.sort_order,
            )
            for payload in payloads
        ]

        colors = await self.uow.product_colors.create_many(colors)

        return [self._to_dto(color) for color in colors]

    async def create(
        self,
        *,
        product_id: UUID,
        name: str,
        sort_order: int = 0,
    ) -> ProductColorDTO:

        color = ProductColor(
            product_id=product_id,
            name=name,
            sort_order=sort_order,
        )

        color = await self.uow.product_colors.create(color)

        return self._to_dto(color)

    async def get_by_id(
        self,
        *,
        color_id: UUID,
    ) -> ProductColorDTO:

        color = await self.uow.product_colors.get_by_id(color_id)

        if color is None:
            raise ProductColorNotFoundError(color_id)

        return self._to_dto(color)

    async def list_by_product(
        self,
        *,
        product_id: UUID,
    ) -> list[ProductColorDTO]:

        colors = await self.uow.product_colors.get_by_product_id(product_id)

        return [self._to_dto(color) for color in colors]

    async def update(
        self,
        *,
        color_id: UUID,
        name: str,
        sort_order: int,
    ) -> ProductColorDTO:

        color = await self.uow.product_colors.get_by_id(color_id)

        if color is None:
            raise ProductColorNotFoundError(color_id)

        color.name = name
        color.sort_order = sort_order

        color = await self.uow.product_colors.update(color)

        await self.uow.commit()
        await self.uow.refresh(color)

        return self._to_dto(color)

    async def update_many(
        self,
        *,
        product_id: UUID,
        payloads: tuple[UpdateProductColorDTO, ...],
    ) -> list[ProductColorDTO]:
        payloads_list = list(payloads)

        existing_colors = await self.uow.product_colors.get_by_product_id(
            product_id=product_id,
        )

        existing_by_id = {color.id: color for color in existing_colors}

        submitted_ids = {
            payload.id for payload in payloads_list if payload.id is not None
        }

        for payload_id in submitted_ids:
            if payload_id not in existing_by_id:
                raise ProductColorNotFoundError(payload_id)

        removed_colors = [
            color for color in existing_colors if color.id not in submitted_ids
        ]

        if removed_colors:
            await self.uow.product_colors.delete_many(
                removed_colors,
            )

        new_colors: list[ProductColor] = []
        updated_colors: list[ProductColor] = []

        for payload in payloads_list:
            if payload.id is None:
                new_colors.append(
                    ProductColor(
                        product_id=product_id,
                        name=payload.name,
                        sort_order=payload.sort_order,
                    )
                )
                continue

            color = existing_by_id[payload.id]

            color.name = payload.name
            color.sort_order = payload.sort_order

            updated_colors.append(color)

        if new_colors:
            await self.uow.product_colors.create_many(
                new_colors,
            )

        if updated_colors:
            await self.uow.product_colors.update_many(
                updated_colors,
            )

        return [self._to_dto(color) for color in [*updated_colors, *new_colors]]

    async def delete(
        self,
        *,
        color_id: UUID,
    ) -> None:

        color = await self.uow.product_colors.get_by_id(color_id)

        if color is None:
            raise ProductColorNotFoundError(color_id)

        await self.uow.product_colors.delete(color)

        await self.uow.commit()

    @staticmethod
    def _to_dto(
        color: ProductColor,
    ) -> ProductColorDTO:
        return ProductColorDTO(
            id=color.id,
            product_id=color.product_id,
            name=color.name,
            sort_order=color.sort_order,
            created_at=color.created_at,
            updated_at=color.updated_at,
        )
