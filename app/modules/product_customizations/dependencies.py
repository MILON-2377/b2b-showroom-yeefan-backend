from fastapi import Depends

from app.core.contracts.services.product_customization import (
    AbstractProductCustomizationService,
)
from app.core.contracts.services.product_customization_option import (
    AbstractProductCustomizationOptionService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_customizations.services.product_customization import (
    ProductCustomizationService,
)
from app.modules.product_customizations.services.product_customization_option import (
    ProductCustomizationOptionService,
)
from app.shared.dependencies import get_uow


def get_product_customization_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractProductCustomizationService:
    return ProductCustomizationService(uow)


def get_product_customization_option_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractProductCustomizationOptionService:
    return ProductCustomizationOptionService(uow)
