from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.product_customization_option import (
    AbstractProductCustomizationOptionRepository,
)
from app.modules.product_customizations.models.product_customization_option import (
    ProductCustomizationOption,
)


class ProductCustomizationOptionRepository(
    AbstractProductCustomizationOptionRepository
):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        option: ProductCustomizationOption,
    ) -> ProductCustomizationOption:
        self.session.add(option)

        await self.session.flush()
        await self.session.refresh(option)

        return option

    async def get_by_id(
        self,
        option_id: UUID,
    ) -> ProductCustomizationOption | None:
        result = await self.session.execute(
            select(ProductCustomizationOption).where(
                ProductCustomizationOption.id == option_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_customization_id(
        self,
        customization_id: UUID,
    ) -> list[ProductCustomizationOption]:
        result = await self.session.execute(
            select(ProductCustomizationOption)
            .where(
                ProductCustomizationOption.customization_id
                == customization_id
            )
            .order_by(
                ProductCustomizationOption.sort_order,
                ProductCustomizationOption.option_type,
            )
        )

        return list(result.scalars().all())

    async def update(
        self,
        option: ProductCustomizationOption,
    ) -> ProductCustomizationOption:
        await self.session.flush()
        await self.session.refresh(option)

        return option

    async def delete(
        self,
        option: ProductCustomizationOption,
    ) -> None:
        await self.session.delete(option)
        await self.session.flush()