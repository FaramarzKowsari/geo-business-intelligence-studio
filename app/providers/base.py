from abc import ABC, abstractmethod

from app.models import Business, SearchRequest


class ProviderError(RuntimeError):
    """Raised for expected external-provider failures."""


class BusinessProvider(ABC):
    id: str
    label: str

    @abstractmethod
    async def search(self, request: SearchRequest) -> list[Business]:
        raise NotImplementedError
