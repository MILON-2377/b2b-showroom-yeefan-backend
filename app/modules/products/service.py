from uuid import UUID

from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.products.model import Product
from app.shared.utils.slug import create_slug


class ProductService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create(
        self,
        *,
        brand_id: UUID,
        collection_id: UUID,
        category_id: UUID,
        product_code: str,
        name: str,
        description: str | None = None,
        status: RecordStatus = RecordStatus.DRAFT,
        published_at=None,
    ) -> Product:
        brand = await self.uow.brands.get_by_id(brand_id)

        if brand is None:
            raise ValueError(f"Brand '{brand_id}' not found")

        collection = await self.uow.collections.get_by_id(collection_id)

        if collection is None:
            raise ValueError(f"Collection '{collection_id}' not found")

        if collection.brand_id != brand_id:
            raise ValueError(
                f"Collection '{collection_id}' does not belong to brand '{brand_id}'"
            )

        category = await self.uow.categories.get_by_id(category_id)

        if category is None:
            raise ValueError(f"Category '{category_id}' not found")

        if await self.uow.products.exists_by_product_code(
            brand_id,
            product_code,
        ):
            raise ValueError(
                f"Product code '{product_code}' already exists for brand '{brand_id}'"
            )

        slug = create_slug(name)

        if await self.uow.products.exists_by_slug(
            brand_id,
            slug,
        ):
            raise ValueError(
                f"Product slug '{slug}' already exists for brand '{brand_id}'"
            )

        product = Product(
            brand_id=brand_id,
            collection_id=collection_id,
            category_id=category_id,
            product_code=product_code,
            name=name,
            slug=slug,
            description=description,
            status=status,
            published_at=published_at,
        )

        await self.uow.products.add(product)
        await self.uow.commit()

        return product

    async def get_by_id(
        self,
        product_id: UUID,
    ) -> Product | None:
        return await self.uow.products.get_by_id(product_id)

    async def get_by_slug(
        self,
        brand_id: UUID,
        slug: str,
    ) -> Product | None:
        return await self.uow.products.get_by_slug(
            brand_id,
            slug,
        )

    async def get_by_product_code(
        self,
        brand_id: UUID,
        product_code: str,
    ) -> Product | None:
        return await self.uow.products.get_by_product_code(
            brand_id,
            product_code,
        )

    async def list(
        self,
        *,
        brand_id: UUID | None = None,
        collection_id: UUID | None = None,
        category_id: UUID | None = None,
        status: RecordStatus | None = None,
    ) -> list[Product]:
        return await self.uow.products.list(
            brand_id=brand_id,
            collection_id=collection_id,
            category_id=category_id,
            status=status,
        )

    async def delete(
        self,
        product_id: UUID,
    ) -> None:
        product = await self.uow.products.get_by_id(product_id)

        if product is None:
            raise ValueError(f"Product '{product_id}' not found")

        await self.uow.products.delete(product)
        await self.uow.commit()
