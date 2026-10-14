from abc import ABC, abstractmethod


class AbstractHashTokenManager(ABC):
    @abstractmethod
    def hash_token(self, token: str) -> str: ...

    @abstractmethod
    def verify_token(
        self,
        token: str,
        hashed_token: str,
    ) -> bool: ...
