import json
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from app.core.contracts.ai.service import AbstractAIService
from app.core.security.rate_limiter import limiter
from app.modules.ai.dependencies import get_ai_service
from app.modules.ai.schemas import AIChatRequest, AIChatResponse

router = APIRouter(prefix="/ai", tags=["Public AI"])


@router.post("/chat", response_model=AIChatResponse)
@limiter.limit("10/minute")
async def chat_with_ai(
    request: AIChatRequest,
    ai_service: Annotated[
        AbstractAIService,
        Depends(get_ai_service),
    ],
) -> AIChatResponse:
    result = await ai_service.chat(request.to_dto())

    return AIChatResponse(content=result.content or "")


@router.post("/chat/stream")
@limiter.limit("10/minute")
async def chat_with_ai_stream(
    request: AIChatRequest,
    ai_service: Annotated[
        AbstractAIService,
        Depends(get_ai_service),
    ],
) -> StreamingResponse:

    async def generate_events() -> AsyncIterator[str]:
        try:
            async for chunk in ai_service.chat_stream(request.to_dto()):
                yield (
                    f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
                )

            yield 'data: {"done": true}\n\n'

        except Exception:
            yield (
                "event: error\n"
                'data: {"message": "The AI service is temporarily unavailable."}\n\n'
            )

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
