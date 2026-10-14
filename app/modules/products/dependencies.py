from fastapi import Depends

from app.core.contracts.services.brand import AbstractBrandService
from app.core.contracts.services.category import AbstractCategoryService
from app.core.contracts.services.collection import AbstractCollectionService
from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.services.product import AbstractProductService
from app.core.contracts.services.product_color import AbstractProductColorService
from app.core.contracts.services.product_customization import (
    AbstractProductCustomizationService,
)
from app.core.contracts.services.product_detail import AbstractProductDetailService
from app.core.contracts.services.product_measurement_guide import (
    AbstractProductMeasurementGuideService,
)
from app.core.contracts.services.product_media import AbstractProductMediaService
from app.core.contracts.services.product_size import AbstractProductSizeService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.brands.dependencies import get_brand_service
from app.modules.categories.dependencies import get_category_service
from app.modules.collections.dependencies import get_collection_service
from app.modules.media.dependencies import get_media_upload_service
from app.modules.product_colors.dependencies import get_product_color_service
from app.modules.product_customizations.dependencies import (
    get_product_customization_service,
)
from app.modules.product_details.dependencies import get_product_detail_service
from app.modules.product_media.dependencies import get_product_media_service
from app.modules.product_sizes.dependencies import (
    get_product_measurement_guide_service,
    get_product_size_service,
)
from app.modules.products.service import ProductService
from app.shared.dependencies import get_uow


def get_product_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    brand_service: AbstractBrandService = Depends(get_brand_service),
    collection_service: AbstractCollectionService = Depends(get_collection_service),
    category_service: AbstractCategoryService = Depends(get_category_service),
    product_media_service: AbstractProductMediaService = Depends(
        get_product_media_service
    ),
    product_detail_service: AbstractProductDetailService = Depends(
        get_product_detail_service
    ),
    product_color_service: AbstractProductColorService = Depends(
        get_product_color_service
    ),
    product_size_service: AbstractProductSizeService = Depends(
        get_product_size_service
    ),
    product_measurement_guide_service: AbstractProductMeasurementGuideService = Depends(
        get_product_measurement_guide_service
    ),
    product_customization_service: AbstractProductCustomizationService = Depends(
        get_product_customization_service
    ),
    media_upload_service: AbstractMediaUploadService = Depends(
        get_media_upload_service
    ),
) -> AbstractProductService:
    return ProductService(
        uow=uow,
        brand_service=brand_service,
        collection_service=collection_service,
        category_service=category_service,
        product_media_service=product_media_service,
        product_detail_service=product_detail_service,
        product_color_service=product_color_service,
        product_size_service=product_size_service,
        product_measurement_guide_service=product_measurement_guide_service,
        product_customization_service=product_customization_service,
        media_upload_service=media_upload_service,
    )
