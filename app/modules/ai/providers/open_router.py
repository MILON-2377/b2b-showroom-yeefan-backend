import json
from collections.abc import AsyncIterator
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.contracts.ai.provider import AbstractAIProvider
from app.modules.ai.dtos import AIResponseDTO, AIToolCallDTO


class DeepSeekProvider(AbstractAIProvider):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-OpenRouter-Title": "YIFAN BRIDAL",
            },
        )
        self.model = settings.openrouter_model

    async def generate(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> AIResponseDTO:
        request_params: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        if tools:
            request_params["tools"] = tools
            request_params["tool_choice"] = "auto"

        response = await self.client.chat.completions.create(
            **request_params,
        )

        message = response.choices[0].message

        tool_calls = [
            AIToolCallDTO(
                id=tool_call.id,
                name=tool_call.function.name,
                arguments=json.loads(
                    tool_call.function.arguments,
                ),
            )
            for tool_call in (message.tool_calls or [])
        ]

        return AIResponseDTO(
            content=message.content,
            tool_calls=tool_calls,
        )

    async def generate_stream(
        self,
        *,
        messages: list[dict[str, Any]],
    ) -> AsyncIterator[str]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )

        async for chunk in stream:
            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content

            if content:
                yield content
