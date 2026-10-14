from fastapi import Depends

from app.core.contracts.services.review import AbstractReviewService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.reviews.service import ReviewService
from app.shared.dependencies import get_uow


def get_review_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractReviewService:

    return ReviewService(uow=uow)
