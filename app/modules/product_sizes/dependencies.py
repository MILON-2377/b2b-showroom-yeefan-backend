from fastapi import Depends

from app.core.contracts.services.product_measurement_guide import (
    AbstractProductMeasurementGuideService,
)
from app.core.contracts.services.product_size import AbstractProductSizeService
from app.core.contracts.services.size_measurement import (
    AbstractSizeMeasurementService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_sizes.services.product_measurement_guide import (
    ProductMeasurementGuideService,
)
from app.modules.product_sizes.services.product_size import ProductSizeService
from app.modules.product_sizes.services.size_measurement import (
    SizeMeasurementService,
)
from app.shared.dependencies import get_uow


def get_product_size_measurement_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractSizeMeasurementService:
    return SizeMeasurementService(uow=uow)


def get_product_size_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    size_measurement_service: AbstractSizeMeasurementService = Depends(
        get_product_size_measurement_service
    ),
) -> AbstractProductSizeService:
    return ProductSizeService(
        uow=uow,
        size_measurement_service=size_measurement_service,
    )


def get_product_measurement_guide_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractProductMeasurementGuideService:
    return ProductMeasurementGuideService(uow=uow)
