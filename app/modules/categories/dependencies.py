from fastapi import Depends

from app.core.contracts.services.category import AbstractCategoryService
from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.categories.service import CategoryService
from app.modules.media.dependencies import get_media_upload_service
from app.shared.dependencies import get_uow


def get_category_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    media_upload_service: AbstractMediaUploadService = Depends(
        get_media_upload_service
    ),
) -> AbstractCategoryService:
    return CategoryService(uow=uow, media_upload_service=media_upload_service)
