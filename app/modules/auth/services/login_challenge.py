import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core.contracts.services.login_challenge import (
    AbstractLoginChallengeService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.auth.dtos.login_challenge import LoginChallengeVerificationDTO
from app.modules.auth.exceptions import (
    InvalidLoginChallengeError,
    LoginChallengeAttemptsExceededError,
    LoginChallengeExpiredError,
)
from app.modules.auth.models.login_challenge import LoginChallenge


class LoginChallengeService(AbstractLoginChallengeService):
    CODE_LENGTH = 6
    CODE_TTL_MINUTES = 5

    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self.uow = uow

    @staticmethod
    def _generate_code() -> str:
        return f"{secrets.randbelow(10**6):06d}"

    @staticmethod
    def _hash_code(code: str) -> str:
        return hashlib.sha256(code.encode("utf-8")).hexdigest()

    async def create_challenge(
        self,
        *,
        user_id: UUID,
    ) -> tuple[LoginChallenge, str]:
        now = datetime.now(timezone.utc)

        await self.uow.login_challenges.invalidate_active_by_user_id(
            user_id=user_id,
            now=now,
        )

        code = self._generate_code()

        challenge = LoginChallenge(
            user_id=user_id,
            code_hash=self._hash_code(code),
            expires_at=now + timedelta(minutes=self.CODE_TTL_MINUTES),
            attempts=0,
        )

        challenge = await self.uow.login_challenges.create(challenge)

        return challenge, code

    async def verify_challenge(
        self,
        *,
        challenge_id: UUID,
        code: str,
    ) -> LoginChallengeVerificationDTO:
        now = datetime.now(timezone.utc)

        challenge = await self.uow.login_challenges.get_by_id_for_update(
            challenge_id=challenge_id,
        )

        if challenge is None:
            raise InvalidLoginChallengeError()

        if challenge.consumed_at is not None:
            raise InvalidLoginChallengeError()

        if challenge.expires_at <= now:
            raise LoginChallengeExpiredError()

        if challenge.attempts >= self.MAX_ATTEMPTS:
            raise LoginChallengeAttemptsExceededError()

        submitted_hash = self._hash_code(code)

        if not hmac.compare_digest(challenge.code_hash, submitted_hash):
            challenge.attempts += 1

            await self.uow.login_challenges.update(challenge)
            await self.uow.flush()

            if challenge.attempts >= self.MAX_ATTEMPTS:
                return LoginChallengeVerificationDTO(
                    error_code="ATTEMPTS_EXCEEDED",
                )

            return LoginChallengeVerificationDTO(
                error_code="INVALID_CODE",
            )

        challenge.consumed_at = now

        await self.uow.login_challenges.update(challenge)
        await self.uow.flush()

        return LoginChallengeVerificationDTO(
            user_id=challenge.user_id,
        )
