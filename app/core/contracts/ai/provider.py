from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from app.modules.ai.dtos import AIResponseDTO


class AbstractAIProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> AIResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def generate_stream(
        self,
        *,
        messages: list[dict[str, Any]],
    ) -> AsyncIterator[str]:
        raise NotImplementedError
