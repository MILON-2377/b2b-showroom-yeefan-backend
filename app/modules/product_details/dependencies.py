from fastapi import Depends

from app.core.contracts.services.product_detail import AbstractProductDetailService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_details.service import ProductDetailService
from app.shared.dependencies import get_uow


def get_product_detail_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractProductDetailService:
    return ProductDetailService(uow=uow)
