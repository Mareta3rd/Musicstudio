
from __future__ import annotations

from abc import ABC, abstractmethod

from musicstudio.models import GenerationRequest, ProviderCapabilities, ProviderStatus


class MusicProvider(ABC):
    name: str
    capabilities: ProviderCapabilities

    @abstractmethod
    async def submit(self, request: GenerationRequest) -> str:
        """Submit a generation and return the provider job id."""

    @abstractmethod
    async def status(self, provider_job_id: str) -> ProviderStatus:
        """Return normalized provider job status."""

    async def close(self) -> None:
        """Optional provider cleanup hook."""
