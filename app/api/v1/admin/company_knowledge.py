from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response, status

from app.core.contracts.services.company_knowledge import (
    AbstractCompanyKnowledgeService,
)
from app.core.models import RecordStatus
from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.core.security.rate_limiter import limiter
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.company_knowledge.dependencies import (
    get_company_knowledge_service,
)
from app.modules.company_knowledge.dtos import (
    CreateCompanyKnowledgeDTO,
    UpdateCompanyKnowledgeDTO,
)
from app.modules.company_knowledge.schemas import (
    CompanyKnowledgeListResponse,
    CompanyKnowledgeResponse,
    CreateCompanyKnowledgeRequest,
    UpdateCompanyKnowledgeRequest,
)
from app.modules.company_knowledge.service import CompanyKnowledgeService

router = APIRouter(
    prefix="/company-knowledges",
    tags=["admin-company-knowledges"],
)


@router.post(
    "",
    response_model=CompanyKnowledgeResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("60/minute")
async def create_company_knowledge(
    request: Request,
    payload: CreateCompanyKnowledgeRequest,
    service: Annotated[
        AbstractCompanyKnowledgeService,
        Depends(get_company_knowledge_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COMPANY_KNOWLEDGE_MANAGE)),
    ],
) -> CompanyKnowledgeResponse:
    knowledge = await service.create(
        CreateCompanyKnowledgeDTO(
            title=payload.title,
            category=payload.category,
            content=payload.content,
        )
    )
    return CompanyKnowledgeResponse.model_validate(knowledge)


@router.get(
    "",
    response_model=CompanyKnowledgeListResponse,
)
@limiter.limit("120/minute")
async def list_company_knowledge(
    request: Request,
    service: Annotated[
        AbstractCompanyKnowledgeService,
        Depends(get_company_knowledge_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COMPANY_KNOWLEDGE_READ)),
    ],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    record_status: RecordStatus | None = Query(
        default=None,
        alias="status",
    ),
) -> CompanyKnowledgeListResponse:
    items, total = await service.list_admin(
        page=page,
        page_size=page_size,
        search=search,
        status=record_status,
    )

    return CompanyKnowledgeListResponse(
        items=[CompanyKnowledgeResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{knowledge_id}",
    response_model=CompanyKnowledgeResponse,
)
@limiter.limit("120/minute")
async def get_company_knowledge(
    request: Request,
    knowledge_id: UUID,
    service: Annotated[
        AbstractCompanyKnowledgeService,
        Depends(get_company_knowledge_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COMPANY_KNOWLEDGE_READ)),
    ],
) -> CompanyKnowledgeResponse:
    knowledge = await service.get_by_id(knowledge_id)
    return CompanyKnowledgeResponse.model_validate(knowledge)


@router.patch(
    "/{knowledge_id}",
    response_model=CompanyKnowledgeResponse,
)
@limiter.limit("30/minute")
async def update_company_knowledge(
    request: Request,
    knowledge_id: UUID,
    payload: UpdateCompanyKnowledgeRequest,
    service: Annotated[
        AbstractCompanyKnowledgeService,
        Depends(get_company_knowledge_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COMPANY_KNOWLEDGE_MANAGE)),
    ],
) -> CompanyKnowledgeResponse:
    knowledge = await service.update(
        knowledge_id,
        UpdateCompanyKnowledgeDTO(**payload.model_dump(exclude_unset=True)),
    )
    return CompanyKnowledgeResponse.model_validate(knowledge)


@router.delete(
    "/{knowledge_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("10/minute")
async def delete_company_knowledge(
    request: Request,
    knowledge_id: UUID,
    service: Annotated[
        AbstractCompanyKnowledgeService,
        Depends(get_company_knowledge_service),
    ],
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.COMPANY_KNOWLEDGE_MANAGE)),
    ],
) -> Response:
    await service.delete(knowledge_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
