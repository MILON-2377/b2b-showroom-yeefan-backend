import hashlib
import hmac

from app.core.config import settings
from app.core.contracts.security.token_hasher import AbstractTokenHasher


class TokenHasher(AbstractTokenHasher):
    def __init__(self) -> None:
        self.secret_key = settings.jwt_secret_key.encode()

    def hash_token(self, token: str) -> str:
        return hmac.new(
            self.secret_key,
            token.encode(),
            hashlib.sha256,
        ).hexdigest()

    def verify_token(
        self,
        token: str,
        token_hash: str,
    ) -> bool:
        expected_hash = self.hash_token(token)

        return hmac.compare_digest(
            expected_hash,
            token_hash,
        )
