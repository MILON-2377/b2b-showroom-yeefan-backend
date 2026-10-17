from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.about_video import AbstractAboutVideoRepository
from app.core.contracts.repositories.auth_refresh_token import (
    AbstractRefreshTokenRepository,
)
from app.core.contracts.repositories.auth_session import AbstractSessionRepository
from app.core.contracts.repositories.brand import AbstractBrandRepository
from app.core.contracts.repositories.catalog import AbstractCatalogRepository
from app.core.contracts.repositories.category import (
    AbstractCategoryRepository,
)
from app.core.contracts.repositories.collection import AbstractCollectionRepository
from app.core.contracts.repositories.company_knowledge import (
    AbstractCompanyKnowledgeRepository,
)
from app.core.contracts.repositories.dashboard import AbstractDashboardRepository
from app.core.contracts.repositories.inquiry import AbstractInquiryRepository
from app.core.contracts.repositories.inquiry_product import (
    AbstractInquiryProductRepository,
)
from app.core.contracts.repositories.login_challenge import (
    AbstractLoginChallengeRepository,
)
from app.core.contracts.repositories.media_asset import AbstractMediaAssetRepository
from app.core.contracts.repositories.product import (
    AbstractProductRepository,
)
from app.core.contracts.repositories.product_color import AbstractProductColorRepository
from app.core.contracts.repositories.product_customization import (
    AbstractProductCustomizationRepository,
)
from app.core.contracts.repositories.product_customization_option import (
    AbstractProductCustomizationOptionRepository,
)
from app.core.contracts.repositories.product_detail import (
    AbstractProductDetailRepository,
)
from app.core.contracts.repositories.product_measurement_guide import (
    AbstractProductMeasurementGuideRepository,
)
from app.core.contracts.repositories.product_media import AbstractProductMediaRepository
from app.core.contracts.repositories.product_size import AbstractProductSizeRepository
from app.core.contracts.repositories.review import AbstractReviewRepository
from app.core.contracts.repositories.size_measurement import (
    AbstractSizeMeasurementRepository,
)
from app.core.contracts.repositories.upload_session import (
    AbstractUploadSessionRepository,
)
from app.core.contracts.repositories.user import AbstractUserRepository
from app.core.contracts.repositories.user_profile import AbstractUserProfileRepository
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.about_videos.repository import AboutVideoRepository
from app.modules.auth.repositories.login_challenge import LoginChallengeRepository
from app.modules.auth.repositories.refresh_token import RefreshTokenRepository
from app.modules.auth.repositories.session import SessionRepository
from app.modules.auth.repositories.user import UserRepository
from app.modules.auth.repositories.user_profile import UserProfileRepository
from app.modules.brands.repository import BrandRepository
from app.modules.catalogs.repository import CatalogRepository
from app.modules.categories.repository import CategoryRepository
from app.modules.collections.repository import CollectionRepository
from app.modules.company_knowledge.repository import CompanyKnowledgeRepository
from app.modules.dashboard.repository import DashboardRepository
from app.modules.inquiries.repositories.inquiry import InquiryRepository
from app.modules.inquiries.repositories.inquiry_product import InquiryProductRepository
from app.modules.media.repository import MediaAssetRepository, UploadSessionRepository
from app.modules.product_colors.repository import (
    ProductColorRepository,
)
from app.modules.product_customizations.repositories.product_customization import (
    ProductCustomizationRepository,
)
from app.modules.product_customizations.repositories.product_customization_option import (
    ProductCustomizationOptionRepository,
)
from app.modules.product_details.repository import ProductDetailRepository
from app.modules.product_media.repository import ProductMediaRepository
from app.modules.product_sizes.repositories.product_measurement_guide import (
    ProductMeasurementGuideRepository,
)
from app.modules.product_sizes.repositories.product_size import ProductSizeRepository
from app.modules.product_sizes.repositories.size_measurement import (
    SizeMeasurementRepository,
)
from app.modules.products.repository import ProductRepository
from app.modules.reviews.repository import ReviewRepository


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):

        self.session = session

        self._login_challenge_repository: AbstractLoginChallengeRepository | None = None
        self._dashboard_repository: AbstractDashboardRepository | None = None
        self._about_video_repository: AbstractAboutVideoRepository | None = None
        self._company_knowledge_repository: (
            AbstractCompanyKnowledgeRepository | None
        ) = None
        self._catalog_repository: AbstractCatalogRepository | None = None
        self._review_repository: AbstractReviewRepository | None = None
        self._inquiry_repository: AbstractInquiryRepository | None = None
        self._inquiry_product_repository: AbstractInquiryProductRepository | None = None
        self._brand_repository: AbstractBrandRepository | None = None
        self._collection_repository: AbstractCollectionRepository | None = None
        self._category_repository: AbstractCategoryRepository | None = None
        self._media_asset_repository: AbstractMediaAssetRepository | None = None
        self._product_media_repository: AbstractProductMediaRepository | None = None
        self._upload_session_repository: AbstractUploadSessionRepository | None = None
        self._users_repository: AbstractUserRepository | None = None
        self._refresh_token_repository: AbstractRefreshTokenRepository | None = None
        self._auth_session_repository: AbstractSessionRepository | None = None
        self._user_profile_repository: AbstractUserProfileRepository | None = None
        self._product_details_repository: AbstractProductDetailRepository | None = None
        self._product_size_repository: AbstractProductSizeRepository | None = None
        self._size_measurement_repository: AbstractSizeMeasurementRepository | None = (
            None
        )
        self._product_measurement_guide_repository: (
            AbstractProductMeasurementGuideRepository | None
        ) = None
        self._product_color_repository: AbstractProductColorRepository | None = None
        self._product_customization_repository: (
            AbstractProductCustomizationRepository | None
        ) = None
        self._product_customization_option_repository: (
            AbstractProductCustomizationOptionRepository | None
        ) = None

        self._product_repository: AbstractProductRepository | None = None

    @property
    def login_challenges(self) -> AbstractLoginChallengeRepository:
        if self._login_challenge_repository is None:
            self._login_challenge_repository = LoginChallengeRepository(self.session)
        return self._login_challenge_repository

    @property
    def dashboard(self) -> AbstractDashboardRepository:
        if self._dashboard_repository is None:
            self._dashboard_repository = DashboardRepository(self.session)
        return self._dashboard_repository

    @property
    def about_videos(self) -> AbstractAboutVideoRepository:
        if self._about_video_repository is None:
            self._about_video_repository = AboutVideoRepository(self.session)
        return self._about_video_repository

    @property
    def company_knowledges(self) -> AbstractCompanyKnowledgeRepository:
        if self._company_knowledge_repository is None:
            self._company_knowledge_repository = CompanyKnowledgeRepository(
                self.session
            )
        return self._company_knowledge_repository

    @property
    def catalogs(self) -> AbstractCatalogRepository:
        if self._catalog_repository is None:
            self._catalog_repository = CatalogRepository(self.session)
        return self._catalog_repository

    @property
    def reviews(self) -> AbstractReviewRepository:
        if self._review_repository is None:
            self._review_repository = ReviewRepository(self.session)
        return self._review_repository

    @property
    def inquiries(self) -> AbstractInquiryRepository:
        if self._inquiry_repository is None:
            self._inquiry_repository = InquiryRepository(self.session)

        return self._inquiry_repository

    @property
    def inquiry_products(self) -> AbstractInquiryProductRepository:
        if self._inquiry_product_repository is None:
            self._inquiry_product_repository = InquiryProductRepository(self.session)

        return self._inquiry_product_repository

    @property
    def products(self) -> AbstractProductRepository:
        if self._product_repository is None:
            self._product_repository = ProductRepository(self.session)

        return self._product_repository

    @property
    def product_customizations(self) -> AbstractProductCustomizationRepository:
        if self._product_customization_repository is None:
            self._product_customization_repository = ProductCustomizationRepository(
                self.session
            )

        return self._product_customization_repository

    @property
    def product_customization_options(
        self,
    ) -> AbstractProductCustomizationOptionRepository:
        if self._product_customization_option_repository is None:
            self._product_customization_option_repository = (
                ProductCustomizationOptionRepository(self.session)
            )

        return self._product_customization_option_repository

    @property
    def product_colors(self) -> AbstractProductColorRepository:
        if self._product_color_repository is None:
            self._product_color_repository = ProductColorRepository(self.session)

        return self._product_color_repository

    @property
    def product_measurement_guides(self) -> AbstractProductMeasurementGuideRepository:
        if self._product_measurement_guide_repository is None:
            self._product_measurement_guide_repository = (
                ProductMeasurementGuideRepository(self.session)
            )

        return self._product_measurement_guide_repository

    @property
    def size_measurements(self) -> AbstractSizeMeasurementRepository:
        if self._size_measurement_repository is None:
            self._size_measurement_repository = SizeMeasurementRepository(self.session)

        return self._size_measurement_repository

    @property
    def product_sizes(self) -> AbstractProductSizeRepository:

        if self._product_size_repository is None:
            self._product_size_repository = ProductSizeRepository(self.session)

        return self._product_size_repository

    @property
    def product_details(self) -> AbstractProductDetailRepository:
        if self._product_details_repository is None:
            self._product_details_repository = ProductDetailRepository(self.session)

        return self._product_details_repository

    @property
    def user_profiles(self) -> AbstractUserProfileRepository:
        if self._user_profile_repository is None:
            self._user_profile_repository = UserProfileRepository(self.session)

        return self._user_profile_repository

    @property
    def users(self) -> AbstractUserRepository:
        if self._users_repository is None:
            self._users_repository = UserRepository(self.session)

        return self._users_repository

    @property
    def auth_sessions(self) -> AbstractSessionRepository:

        if self._auth_session_repository is None:
            self._auth_session_repository = SessionRepository(self.session)

        return self._auth_session_repository

    @property
    def refresh_tokens(self) -> AbstractRefreshTokenRepository:
        if self._refresh_token_repository is None:
            self._refresh_token_repository = RefreshTokenRepository(self.session)

        return self._refresh_token_repository

    @property
    def brands(self) -> AbstractBrandRepository:
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
        if self._upload_session_repository is None:
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
            if self.session.in_transaction():
                await self.rollback()

        finally:
            await self.session.close()
