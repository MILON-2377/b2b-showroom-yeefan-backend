from abc import ABC, abstractmethod


class AbstractTokenHasher(ABC):
    @abstractmethod
    def hash_token(self, token: str) -> str: ...

    @abstractmethod
    def verify_token(
        self,
        token: str,
        token_hash: str,
    ) -> bool: ...
