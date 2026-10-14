from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.modules.ai.dtos import AIChatDTO, AIResponseDTO


class AbstractAIService(ABC):
    @abstractmethod
    async def chat(
        self,
        data: AIChatDTO,
    ) -> AIResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def chat_stream(
        self,
        data: AIChatDTO,
    ) -> AsyncIterator[str]:
        raise NotImplementedError
