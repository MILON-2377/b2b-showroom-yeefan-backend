from fastapi import APIRouter

from app.api.v1.admin.routes import admin_router
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.public.routes import public_api

api_router = APIRouter(prefix="/api/v1")


# Auth Router
api_router.include_router(auth_router)

# Admin Router
api_router.include_router(admin_router)


# Public Router
api_router.include_router(public_api)
