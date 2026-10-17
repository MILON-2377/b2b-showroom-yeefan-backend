from abc import ABC, abstractmethod

from app.core.contracts.repositories.about_video import AbstractAboutVideoRepository
from app.core.contracts.repositories.auth_refresh_token import (
    AbstractRefreshTokenRepository,
)
from app.core.contracts.repositories.auth_session import AbstractSessionRepository
from app.core.contracts.repositories.brand import AbstractBrandRepository
from app.core.contracts.repositories.catalog import AbstractCatalogRepository
from app.core.contracts.repositories.category import AbstractCategoryRepository
from app.core.contracts.repositories.collection import AbstractCollectionRepository
from app.core.contracts.repositories.company_knowledge import (
    AbstractCompanyKnowledgeRepository,
)
from app.core.contracts.repositories.dashboard import (
    AbstractDashboardRepository,
)
from app.core.contracts.repositories.inquiry import AbstractInquiryRepository
from app.core.contracts.repositories.inquiry_product import (
    AbstractInquiryProductRepository,
)
from app.core.contracts.repositories.login_challenge import (
    AbstractLoginChallengeRepository,
)
from app.core.contracts.repositories.media_asset import (
    AbstractMediaAssetRepository,
)
from app.core.contracts.repositories.product import AbstractProductRepository
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


class AbstractUnitOfWork(ABC):
    @property
    @abstractmethod
    def login_challenges(self) -> AbstractLoginChallengeRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def dashboard(self) -> AbstractDashboardRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def about_videos(self) -> AbstractAboutVideoRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def company_knowledges(self) -> AbstractCompanyKnowledgeRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def catalogs(self) -> AbstractCatalogRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def reviews(self) -> AbstractReviewRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def inquiries(self) -> AbstractInquiryRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def inquiry_products(self) -> AbstractInquiryProductRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def categories(self) -> AbstractCategoryRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def products(
        self,
    ) -> AbstractProductRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def product_media(
        self,
    ) -> AbstractProductMediaRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def product_customizations(
        self,
    ) -> AbstractProductCustomizationRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def product_customization_options(
        self,
    ) -> AbstractProductCustomizationOptionRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def product_colors(self) -> AbstractProductColorRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def product_measurement_guides(
        self,
    ) -> AbstractProductMeasurementGuideRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def size_measurements(self) -> AbstractSizeMeasurementRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def product_sizes(self) -> AbstractProductSizeRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def product_details(self) -> AbstractProductDetailRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def user_profiles(self) -> AbstractUserProfileRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def users(self) -> AbstractUserRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def auth_sessions(self) -> AbstractSessionRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def refresh_tokens(self) -> AbstractRefreshTokenRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def brands(self) -> AbstractBrandRepository:
        pass

    @property
    @abstractmethod
    def collections(self) -> AbstractCollectionRepository:
        pass

    @property
    @abstractmethod
    def media_assets(self) -> AbstractMediaAssetRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def upload_sessions(self) -> AbstractUploadSessionRepository:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        pass

    @abstractmethod
    async def refresh(self, entity) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        pass
