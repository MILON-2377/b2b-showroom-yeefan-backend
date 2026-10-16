from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from app.core.contracts.repositories.catalog import AbstractCatalogRepository
from app.core.models import RecordStatus
from app.modules.catalogs.model import Catalog
from app.modules.media.model import MediaAsset, MediaAssetStatus, MediaType


class CatalogRepository(AbstractCatalogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        collection_id: UUID | None = None,
        status: RecordStatus | None = None,
        sort_order: str = "desc",
    ) -> tuple[
        list[tuple[Catalog, MediaAsset, MediaAsset]],
        int,
    ]:
        pdf_asset = aliased(MediaAsset)
        cover_asset = aliased(MediaAsset)

        filters = [
            pdf_asset.secure_url.is_not(None),
            cover_asset.secure_url.is_not(None),
        ]

        if collection_id is not None:
            filters.append(Catalog.collection_id == collection_id)

        if status is not None:
            filters.append(Catalog.status == status)

        if search:
            pattern = f"%{search.strip()}%"

            filters.append(
                or_(
                    Catalog.title.ilike(pattern),
                    Catalog.description.ilike(pattern),
                )
            )

        count_statement = (
            select(func.count(Catalog.id))
            .select_from(Catalog)
            .join(
                pdf_asset,
                Catalog.pdf_media_asset_id == pdf_asset.id,
            )
            .join(
                cover_asset,
                Catalog.cover_media_asset_id == cover_asset.id,
            )
            .where(*filters)
        )

        total = await self.session.scalar(count_statement) or 0

        order_column = (
            Catalog.created_at.asc()
            if sort_order == "asc"
            else Catalog.created_at.desc()
        )

        statement = (
            select(
                Catalog,
                pdf_asset,
                cover_asset,
            )
            .select_from(Catalog)
            .join(
                pdf_asset,
                Catalog.pdf_media_asset_id == pdf_asset.id,
            )
            .join(
                cover_asset,
                Catalog.cover_media_asset_id == cover_asset.id,
            )
            .where(*filters)
            .order_by(
                order_column,
                Catalog.id.asc(),
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(statement)

        return list(result.tuples().all()), total

    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        collection_id: UUID | None = None,
        sort_order: str = "desc",
    ) -> tuple[list[tuple[Catalog, MediaAsset, MediaAsset]], int]:
        pdf_asset = aliased(MediaAsset)
        cover_asset = aliased(MediaAsset)

        filters = [
            pdf_asset.status == MediaAssetStatus.READY,
            pdf_asset.media_type == MediaType.PDF,
            pdf_asset.mime_type == "application/pdf",
            pdf_asset.secure_url.is_not(None),
            cover_asset.status == MediaAssetStatus.READY,
            cover_asset.media_type == MediaType.IMAGE,
            cover_asset.mime_type.like("image/%"),
            cover_asset.secure_url.is_not(None),
        ]

        if collection_id is not None:
            filters.append(Catalog.collection_id == collection_id)

        if search:
            pattern = f"%{search.strip()}%"
            filters.append(
                or_(
                    Catalog.title.ilike(pattern),
                    Catalog.description.ilike(pattern),
                )
            )

        count_statement = (
            select(func.count(Catalog.id))
            .join(
                pdf_asset,
                Catalog.pdf_media_asset_id == pdf_asset.id,
            )
            .join(
                cover_asset,
                Catalog.cover_media_asset_id == cover_asset.id,
            )
            .where(*filters)
        )

        total = await self.session.scalar(count_statement) or 0

        order_column = (
            Catalog.created_at.asc()
            if sort_order == "asc"
            else Catalog.created_at.desc()
        )

        statement = (
            select(Catalog, pdf_asset, cover_asset)
            .join(
                pdf_asset,
                Catalog.pdf_media_asset_id == pdf_asset.id,
            )
            .join(
                cover_asset,
                Catalog.cover_media_asset_id == cover_asset.id,
            )
            .where(*filters)
            .order_by(order_column, Catalog.id.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(statement)

        return list(result.tuples().all()), total

    async def get_by_id(
        self,
        catalog_id: UUID,
    ) -> Catalog | None:
        stmt = (
            select(Catalog)
            .options(
                selectinload(Catalog.pdf_media_asset),
                selectinload(Catalog.cover_media_asset),
            )
            .where(Catalog.id == catalog_id)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_collection_id(
        self,
        collection_id: UUID,
    ) -> Catalog | None:
        stmt = select(Catalog).where(Catalog.collection_id == collection_id)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create(
        self,
        catalog: Catalog,
    ) -> Catalog:
        self.session.add(catalog)

        await self.session.flush()

        return catalog

    async def update(
        self,
        catalog: Catalog,
    ) -> Catalog:
        await self.session.flush()

        return catalog

    async def delete(
        self,
        catalog: Catalog,
    ) -> None:
        await self.session.delete(catalog)

        await self.session.flush()
