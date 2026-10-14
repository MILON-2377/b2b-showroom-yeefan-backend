from typing import Any
from uuid import UUID

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings
from app.core.contracts.security.jwt_manager import AbstractJwtManager
from app.modules.auth.exceptions import AccessTokenExpiredError


class JwtManager(AbstractJwtManager):
    def __init__(self) -> None:
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm

    def create_access_token(
        self,
        *,
        subject: str,
        session_id: UUID,
        expires_at,
    ) -> str:
        payload = {
            "sub": subject,
            "sid": str(session_id),
            "type": "access",
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, Any] | None:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            if payload.get("type") != "access":
                return None

            return payload

        except ExpiredSignatureError:
            raise AccessTokenExpiredError()

        except JWTError:
            return None
