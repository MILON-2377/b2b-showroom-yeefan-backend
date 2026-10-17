from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.dtos.login_challenge import LoginChallengeVerificationDTO
from app.modules.auth.models.login_challenge import LoginChallenge


class AbstractLoginChallengeService(ABC):
    @abstractmethod
    async def create_challenge(
        self,
        *,
        user_id: UUID,
    ) -> tuple[LoginChallenge, str]:
        raise NotImplementedError

    @abstractmethod
    async def verify_challenge(
        self,
        *,
        challenge_id: UUID,
        code: str,
    ) -> LoginChallengeVerificationDTO:
        raise NotImplementedError
