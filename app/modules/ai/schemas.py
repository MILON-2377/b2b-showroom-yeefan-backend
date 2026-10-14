from pydantic import BaseModel, Field

from app.modules.ai.dtos import AIChatDTO, AIMessageDTO


class AIChatMessageRequest(BaseModel):
    role: str = Field(pattern="^user$")
    content: str = Field(min_length=1, max_length=4000)


class AIChatRequest(BaseModel):
    messages: list[AIChatMessageRequest] = Field(
        min_length=1,
        max_length=20,
    )

    def to_dto(self) -> AIChatDTO:
        return AIChatDTO(
            messages=[
                AIMessageDTO(
                    role=message.role,
                    content=message.content,
                )
                for message in self.messages
            ],
        )


class AIChatResponse(BaseModel):
    content: str
