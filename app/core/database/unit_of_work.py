from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.category import (
    AbstractCategoryRepository,
)
from app.core.contracts.repositories.collection import AbstractCollectionRepository
from app.core.contracts.repositories.media_asset import AbstractMediaAssetRepository
from app.core.contracts.repositories.product import (
    AbstractProductRepository,
)
from app.core.contracts.repositories.product_media import AbstractProductMediaRepository
from app.core.contracts.repositories.upload_session import (
    AbstractUploadSessionRepository,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.brands.repository import BrandRepository
from app.modules.categories.repository import CategoryRepository
from app.modules.collections.repository import CollectionRepository
from app.modules.media.repository import MediaAssetRepository, UploadSessionRepository
from app.modules.product_media.repository import ProductMediaRepository
from app.modules.products.repository import ProductRepository


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):

        self.session = session

        self._brand_repository: BrandRepository | None = None
        self._collection_repository: CollectionRepository | None = None
        self._category_repository: CategoryRepository | None = None
        self._product_repository: ProductRepository | None = None
        self._media_asset_repository: AbstractMediaAssetRepository | None = None
        self._product_media_repository: AbstractProductMediaRepository | None = None
        self._upload_session_repository: AbstractUploadSessionRepository | None = None
        # self._inquiry_repository: InquiryRepository | None = None
        # self._content_repository: ContentRepository | None = None

    @property
    def brands(self) -> BrandRepository:
        if self._brand_repository is None:
            self._brand_repository = BrandRepository(self.session)

        return self._brand_repository

    @property
    def collections(self) -> AbstractCollectionRepository:
        if self._collection_repository is None:
            self._collection_repository = CollectionRepository(self.session)

        return self._collection_repository

    @property
    def categories(self) -> AbstractCategoryRepository:
        if self._category_repository is None:
            self._category_repository = CategoryRepository(self.session)

        return self._category_repository

    @property
    def products(self) -> AbstractProductRepository:
        if self._product_repository is None:
            self._product_repository = ProductRepository(self.session)

        return self._product_repository

    @property
    def media_assets(self) -> AbstractMediaAssetRepository:
        if self._media_asset_repository is None:
            self._media_asset_repository = MediaAssetRepository(self.session)

        return self._media_asset_repository

    @property
    def product_media(self) -> AbstractProductMediaRepository:
        if self._product_media_repository is None:
            self._product_media_repository = ProductMediaRepository(self.session)

        return self._product_media_repository

    @property
    def upload_sessions(self) -> AbstractUploadSessionRepository:
        if self._upload_sessions_repository is None:
            self._upload_session_repository = UploadSessionRepository(self.session)

        return self._upload_session_repository

    async def flush(self) -> None:
        await self.session.flush()

    async def refresh(self, entity) -> None:
        await self.session.refresh(entity)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self) -> "UnitOfWork":

        if not self.session.in_transaction():
            await self.session.begin()

        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        try:
            if exc_type:
                await self.rollback()

        finally:
            await self.session.close()
