import secrets
from datetime import datetime
from uuid import UUID

from app.core.contracts.security.jwt_manager import AbstractJwtManager
from app.core.contracts.security.token_hasher import AbstractTokenHasher
from app.core.contracts.services.token import AbstractTokenService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.security.policies.token_policy import TokenPolicy
from app.modules.auth.dtos.auth import AccessTokenDTO


# Token Service
class TokenService(AbstractTokenService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        jwt_manager: AbstractJwtManager,
        token_hasher: AbstractTokenHasher,
        token_policy: TokenPolicy,
    ):
        self.uow = uow
        self.jwt_manager = jwt_manager
        self.token_hasher = token_hasher
        self.token_policy = token_policy

    def create_access_token(self, subject: str, session_id: UUID) -> AccessTokenDTO:

        expires_at = self.token_policy.access_token_expires_at()

        token = self.jwt_manager.create_access_token(
            subject=subject, session_id=session_id, expires_at=expires_at
        )

        return AccessTokenDTO(token=token, expires_at=expires_at)

    def decode_access_token(self, token: str) -> dict[str, any] | None:
        return self.jwt_manager.decode_access_token(token)

    def generate_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)

    def hash_refresh_token(self, token: str) -> str:
        return self.token_hasher.hash_token(token)

    def refresh_token_expires_at(self, issued_at: datetime) -> datetime:
        return self.token_policy.refresh_token_expires_at(issued_at=issued_at)
