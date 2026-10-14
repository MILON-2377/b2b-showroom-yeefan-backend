from passlib.context import CryptContext

from app.core.contracts.security.hash_token_manager import (
    AbstractHashTokenManager,
)


class HashTokenManager(AbstractHashTokenManager):
    def __init__(self) -> None:
        self.pwd_context = CryptContext(
            schemes=["argon2"],
            deprecated="auto",
        )

    def hash_token(self, token: str) -> str:
        return self.pwd_context.hash(token)

    def verify_token(
        self,
        token: str,
        hashed_token: str,
    ) -> bool:
        return self.pwd_context.verify(
            token,
            hashed_token,
        )
