from fastapi import APIRouter

from .about_videos import router as about_video_router
from .brands import router as brands_router
from .catalogs import router as catalog_router
from .categories import router as category_router
from .collections import router as collections_router
from .company_knowledge import router as company_knowledge_router
from .dashboard import router as dashboard_router
from .inquires import router as inquiry_router
from .products import router as product_router
from .reviews import router as review_router
from .storage import router as storage_router
from .users import router as users_router

admin_router = APIRouter(prefix="/admin")


admin_router.include_router(users_router)

admin_router.include_router(brands_router)
admin_router.include_router(collections_router)
admin_router.include_router(category_router)

admin_router.include_router(product_router)

admin_router.include_router(review_router)

admin_router.include_router(catalog_router)

admin_router.include_router(storage_router)

admin_router.include_router(company_knowledge_router)

admin_router.include_router(inquiry_router)


admin_router.include_router(about_video_router)


admin_router.include_router(dashboard_router)