from fastapi import APIRouter

from app.modules.product_media.router import router as product_media_router

api_router = APIRouter()

api_router.include_router(product_media_router)
