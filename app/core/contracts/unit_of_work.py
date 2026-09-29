from abc import ABC, abstractmethod

from app.core.contracts.repositories.brand import AbstractBrandRepository


class AbstractUnitOfWork(ABC):
    @property
    @abstractmethod
    def brands(self) -> AbstractBrandRepository:
        pass

    @abstractmethod
    async def flush(self) -> None:
        pass

    @abstractmethod
    async def refresh(self, entity) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        pass
