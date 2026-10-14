from fastapi import APIRouter

from app.api.v1.public.about_videos import router as about_video_router
from app.api.v1.public.ai import router as ai_router
from app.api.v1.public.brands import router as brand_router
from app.api.v1.public.catalogs import router as catalog_router
from app.api.v1.public.categories import router as category_router
from app.api.v1.public.collections import router as collection_router
from app.api.v1.public.inquiries import router as inquiry_router
from app.api.v1.public.products import router as product_router
from app.api.v1.public.reviews import router as review_router

public_api = APIRouter(prefix="/public", tags=["Public"])


public_api.include_router(inquiry_router)
public_api.include_router(category_router)
public_api.include_router(product_router)
public_api.include_router(review_router)
public_api.include_router(catalog_router)
public_api.include_router(collection_router)
public_api.include_router(brand_router)
public_api.include_router(ai_router)
public_api.include_router(about_video_router)
