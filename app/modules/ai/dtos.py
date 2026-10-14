from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AIMessageDTO:
    role: str
    content: str


@dataclass(frozen=True)
class AIToolCallDTO:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class AIResponseDTO:
    content: str | None
    tool_calls: list[AIToolCallDTO]


@dataclass(frozen=True)
class AIChatDTO:
    messages: list[AIMessageDTO]
