
import pytest

from musicstudio.models import GenerationRequest, JobStatus
from musicstudio.orchestrator import MusicOrchestrator
from musicstudio.providers.mock import MockProvider


@pytest.mark.asyncio
async def test_mock_generation_completes():
    provider = MockProvider()
    orchestrator = MusicOrchestrator(provider)

    request = GenerationRequest(
        prompt="cinematic Mediterranean night, warm strings and pulse",
        duration=20,
        bpm=112,
    )

    job = await orchestrator.create_job(request)
    assert job.status == JobStatus.queued

    refreshed = await orchestrator.get_job(job.id)
    assert refreshed is not None
    assert refreshed.status == JobStatus.completed
    assert refreshed.metadata["duration"] == 20


@pytest.mark.asyncio
async def test_empty_prompt_is_rejected():
    with pytest.raises(ValueError):
        GenerationRequest(prompt="   ")


@pytest.mark.asyncio
async def test_provider_failure_is_recorded():
    class BrokenProvider(MockProvider):
        async def submit(self, request):
            raise RuntimeError("simulated failure")

    orchestrator = MusicOrchestrator(BrokenProvider())
    job = await orchestrator.create_job(GenerationRequest(prompt="test"))
    assert job.status == JobStatus.failed
    assert "simulated failure" in (job.error or "")
