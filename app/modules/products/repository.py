import base64
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import ColumnElement, and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.contracts.repositories.product import (
    AbstractProductRepository,
)
from app.core.models import RecordStatus
from app.modules.product_media.model import ProductMedia
from app.modules.product_sizes.models.product_size import ProductSize
from app.modules.products.cursor import ProductCursorCodec
from app.modules.products.dtos import (
    ProductCursor,
    ProductQueryDTO,
    ProductSortBy,
    ProductSortOrder,
    PublicProductListResult,
    PublicProductQueryDTO,
)
from app.modules.products.exceptions import InvalidProductCursorError
from app.modules.products.model import Product
from app.modules.products.query import ProductListResult


class ProductRepository(AbstractProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        product_id: UUID,
    ) -> Product | None:

        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(Product.media).selectinload(ProductMedia.media_asset),
                selectinload(Product.details),
                selectinload(Product.colors),
                selectinload(Product.sizes).selectinload(ProductSize.measurement),
                selectinload(Product.measurement_guide),
                selectinload(Product.customization),
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_public_by_id(
        self,
        product_id: UUID,
    ) -> Product | None:
        stmt = (
            select(Product)
            .where(
                Product.id == product_id,
                Product.status == RecordStatus.PUBLISHED,
            )
            .options(
                selectinload(Product.media).selectinload(ProductMedia.media_asset),
                selectinload(Product.details),
                selectinload(Product.colors),
                selectinload(Product.sizes).selectinload(ProductSize.measurement),
                selectinload(Product.measurement_guide),
                selectinload(Product.customization),
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        brand_id: UUID,
        slug: str,
    ) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.brand_id == brand_id,
                Product.slug == slug,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_product_code(
        self,
        brand_id: UUID,
        product_code: str,
    ) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.brand_id == brand_id,
                Product.product_code == product_code,
            )
        )

        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        query: ProductQueryDTO,
    ) -> ProductListResult:

        conditions = []

        if query.search:
            search = f"%{query.search.strip()}%"

            conditions.append(
                or_(
                    Product.name.ilike(search),
                    Product.product_code.ilike(search),
                    Product.slug.ilike(search),
                )
            )

        if query.status is not None:
            conditions.append(Product.status == query.status)

        if query.brand_id is not None:
            conditions.append(Product.brand_id == query.brand_id)

        if query.collection_id is not None:
            conditions.append(Product.collection_id == query.collection_id)

        if query.category_id is not None:
            conditions.append(Product.category_id == query.category_id)

        # -------------------------
        # Total count
        # -------------------------

        count_stmt = select(func.count(Product.id)).where(*conditions)

        total = await self.session.scalar(count_stmt)
        total = total or 0

        # -------------------------
        # Sorting
        # -------------------------

        sort_columns = {
            "created_at": Product.created_at,
            "updated_at": Product.updated_at,
            "name": Product.name,
            "product_code": Product.product_code,
        }

        sort_column = sort_columns[query.sort_by]

        if query.sort_order == "asc":
            order_by = sort_column.asc()
        else:
            order_by = sort_column.desc()

        # -------------------------
        # Pagination
        # -------------------------

        offset = (query.page - 1) * query.page_size

        stmt = (
            select(Product)
            .where(*conditions)
            .options(selectinload(Product.media).selectinload(ProductMedia.media_asset))
            .order_by(order_by)
            .offset(offset)
            .limit(query.page_size)
        )

        result = await self.session.execute(stmt)

        products = list(result.scalars().all())

        return ProductListResult(
            items=products,
            total=total,
        )

    async def exists_by_slug(
        self,
        brand_id: UUID,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool:
        statement = select(Product.id).where(
            Product.brand_id == brand_id,
            Product.slug == slug,
        )

        if exclude_id is not None:
            statement = statement.where(Product.id != exclude_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def exists_by_product_code(
        self,
        brand_id: UUID,
        product_code: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool:
        statement = select(Product.id).where(
            Product.brand_id == brand_id,
            Product.product_code == product_code,
        )

        if exclude_id is not None:
            statement = statement.where(Product.id != exclude_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def create(
        self,
        product: Product,
    ) -> Product:
        self.session.add(product)
        await self.session.flush()
        return product

    async def delete(
        self,
        product: Product,
    ) -> None:
        await self.session.delete(product)

    async def list_featured(
        self,
        *,
        page: int,
        page_size: int,
    ) -> ProductListResult:
        conditions = [
            Product.status == RecordStatus.PUBLISHED,
        ]

        count_stmt = select(func.count(Product.id)).where(*conditions)

        total = await self.session.scalar(count_stmt)
        total = total or 0

        offset = (page - 1) * page_size

        stmt = (
            select(Product)
            .where(*conditions)
            .options(selectinload(Product.media).selectinload(ProductMedia.media_asset))
            .order_by(Product.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        result = await self.session.execute(stmt)

        products = list(result.scalars().all())

        return ProductListResult(
            items=products,
            total=total,
        )

    async def list_public(
        self,
        *,
        query: PublicProductQueryDTO,
    ) -> PublicProductListResult:
        conditions = [
            Product.status == RecordStatus.PUBLISHED,
        ]

        # -------------------------
        # Search
        # -------------------------

        if query.search:
            search = f"%{query.search.strip()}%"

            conditions.append(
                or_(
                    Product.name.ilike(search),
                    Product.product_code.ilike(search),
                    Product.slug.ilike(search),
                )
            )

        # -------------------------
        # Filters
        # -------------------------

        if query.brand_id is not None:
            conditions.append(
                Product.brand_id == query.brand_id,
            )

        if query.collection_id is not None:
            conditions.append(
                Product.collection_id == query.collection_id,
            )

        if query.category_id is not None:
            conditions.append(
                Product.category_id == query.category_id,
            )

        # -------------------------
        # Cursor
        # -------------------------

        if query.cursor:
            cursor = ProductCursorCodec.decode(
                query.cursor,
            )

            if cursor.sort_by != query.sort_by:
                raise InvalidProductCursorError()

            if cursor.sort_order != query.sort_order:
                raise InvalidProductCursorError()

            sort_column = self._public_sort_column(
                query.sort_by,
            )

            conditions.append(
                self._public_cursor_condition(
                    cursor=cursor,
                    sort_column=sort_column,
                )
            )

        # -------------------------
        # Ordering
        # -------------------------

        order_by = self._public_order_by(
            sort_by=query.sort_by,
            sort_order=query.sort_order,
        )

        # -------------------------
        # Fetch one extra row
        # -------------------------

        stmt = (
            select(Product)
            .where(*conditions)
            .options(
                selectinload(Product.media).selectinload(
                    ProductMedia.media_asset,
                ),
            )
            .order_by(*order_by)
            .limit(query.page_size + 1)
        )

        result = await self.session.execute(stmt)

        products = list(
            result.scalars().all(),
        )

        # -------------------------
        # Has more
        # -------------------------

        has_more = len(products) > query.page_size

        if has_more:
            products = products[: query.page_size]

        # -------------------------
        # Next cursor
        # -------------------------

        next_cursor = None

        if has_more and products:
            last_product = products[-1]

            cursor_value = self._public_product_cursor_value(
                product=last_product,
                sort_by=query.sort_by,
            )

            next_cursor = ProductCursorCodec.encode(
                ProductCursor(
                    sort_by=query.sort_by,
                    sort_order=query.sort_order,
                    value=cursor_value,
                    product_id=last_product.id,
                )
            )

        return PublicProductListResult(
            items=tuple(products),
            next_cursor=next_cursor,
            has_more=has_more,
        )

    @staticmethod
    def _encode_public_cursor(
        *,
        created_at: datetime,
        product_id: UUID,
    ) -> str:
        value = f"{created_at.isoformat()}|{product_id}"

        return base64.urlsafe_b64encode(
            value.encode("utf-8"),
        ).decode("utf-8")

    @staticmethod
    def _public_sort_column(
        sort_by: ProductSortBy,
    ) -> ColumnElement[Any]:
        columns = {
            ProductSortBy.CREATED_AT: Product.created_at,
            ProductSortBy.UPDATED_AT: Product.updated_at,
            ProductSortBy.NAME: Product.name,
            ProductSortBy.PRODUCT_CODE: Product.product_code,
        }

        return columns[sort_by]

    @staticmethod
    def _public_cursor_value(
        *,
        cursor: ProductCursor,
    ) -> datetime | str:
        if cursor.sort_by in {
            ProductSortBy.CREATED_AT,
            ProductSortBy.UPDATED_AT,
        }:
            try:
                return datetime.fromisoformat(cursor.value)
            except ValueError as exc:
                raise InvalidProductCursorError() from exc

        return cursor.value

    @staticmethod
    def _public_cursor_condition(
        *,
        cursor: ProductCursor,
        sort_column: ColumnElement[Any],
    ) -> ColumnElement[bool]:
        value = ProductRepository._public_cursor_value(
            cursor=cursor,
        )

        if cursor.sort_order == ProductSortOrder.DESC:
            return or_(
                sort_column < value,
                and_(
                    sort_column == value,
                    Product.id < cursor.product_id,
                ),
            )

        return or_(
            sort_column > value,
            and_(
                sort_column == value,
                Product.id > cursor.product_id,
            ),
        )

    @staticmethod
    def _public_order_by(
        *,
        sort_by: ProductSortBy,
        sort_order: ProductSortOrder,
    ) -> tuple[ColumnElement[Any], ColumnElement[Any]]:
        sort_column = ProductRepository._public_sort_column(
            sort_by,
        )

        if sort_order == ProductSortOrder.DESC:
            return (
                sort_column.desc(),
                Product.id.desc(),
            )

        return (
            sort_column.asc(),
            Product.id.asc(),
        )

    @staticmethod
    def _public_product_cursor_value(
        *,
        product: Product,
        sort_by: ProductSortBy,
    ) -> str:
        if sort_by == ProductSortBy.CREATED_AT:
            return product.created_at.isoformat()

        if sort_by == ProductSortBy.UPDATED_AT:
            return product.updated_at.isoformat()

        if sort_by == ProductSortBy.NAME:
            return product.name

        if sort_by == ProductSortBy.PRODUCT_CODE:
            return product.product_code

        raise InvalidProductCursorError()
