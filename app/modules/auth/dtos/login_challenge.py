from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LoginChallengeDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    challenge_id: UUID
    message: str
    expires_in: int


@dataclass(frozen=True, slots=True)
class LoginChallengeVerificationDTO:
    user_id: UUID | None = None
    error_code: str | None = None

    @property
    def is_valid(self) -> bool:
        return self.user_id is not None
