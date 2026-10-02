
from __future__ import annotations

from hashlib import sha1
from uuid import uuid4

from musicstudio.models import GenerationRequest, JobStatus, ProviderCapabilities, ProviderStatus
from musicstudio.providers.base import MusicProvider


class MockProvider(MusicProvider):
    name = "mock"
    capabilities = ProviderCapabilities(
        name="mock",
        label="Laboratory",
        local=True,
        features=["instant jobs", "UI development", "workflow testing"],
    )

    def __init__(self) -> None:
        self._jobs: dict[str, ProviderStatus] = {}

    async def submit(self, request: GenerationRequest) -> str:
        provider_job_id = str(uuid4())
        fingerprint = sha1(request.prompt.encode("utf-8")).hexdigest()[:8]
        self._jobs[provider_job_id] = ProviderStatus(
            status=JobStatus.completed,
            title=f"{request.prompt[:42]}{'…' if len(request.prompt) > 42 else ''}",
            metadata={
                "mode": "laboratory",
                "fingerprint": fingerprint,
                "duration": request.duration,
                "bpm": request.bpm,
                "key_scale": request.key_scale or "auto",
            },
        )
        return provider_job_id

    async def status(self, provider_job_id: str) -> ProviderStatus:
        return self._jobs.get(
            provider_job_id,
            ProviderStatus(status=JobStatus.failed, error="Mock job not found"),
        )
