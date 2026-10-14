from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.core.contracts.services.dashboard import (
    AbstractDashboardService,
)
from app.core.security.rate_limiter import limiter
from app.modules.dashboard.dependencies import get_dashboard_service
from app.modules.dashboard.schemas import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["admin-dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
@limiter.limit("120/minute")
async def get_dashboard(
    request: Request,
    service: Annotated[
        AbstractDashboardService,
        Depends(get_dashboard_service),
    ],
) -> DashboardResponse:
    dashboard = await service.get_dashboard()

    return DashboardResponse.model_validate(dashboard)