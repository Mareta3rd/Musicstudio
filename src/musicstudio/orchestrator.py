
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from musicstudio.models import GenerationJob, GenerationRequest, JobStatus
from musicstudio.providers.base import MusicProvider


class MusicOrchestrator:
    def __init__(self, provider: MusicProvider) -> None:
        self.provider = provider
        self.jobs: dict[str, GenerationJob] = {}

    async def create_job(self, request: GenerationRequest) -> GenerationJob:
        job_id = str(uuid4())
        try:
            provider_job_id = await self.provider.submit(request)
            job = GenerationJob(
                id=job_id,
                provider=self.provider.name,
                provider_job_id=provider_job_id,
                status=JobStatus.queued,
                request=request,
            )
        except Exception as exc:
            job = GenerationJob(
                id=job_id,
                provider=self.provider.name,
                status=JobStatus.failed,
                request=request,
                error=str(exc),
            )

        self.jobs[job_id] = job
        return job

    async def refresh(self, job_id: str) -> GenerationJob | None:
        job = self.jobs.get(job_id)
        if job is None:
            return None
        if job.status in (JobStatus.completed, JobStatus.failed):
            return job
        if not job.provider_job_id:
            return job

        result = await self.provider.status(job.provider_job_id)
        job.status = result.status
        job.updated_at = datetime.now(timezone.utc)
        if result.title:
            job.title = result.title
        job.metadata.update(result.metadata)
        job.error = result.error
        if result.audio_path:
            job.audio_url = f"/api/jobs/{job.id}/audio"
        return job

    async def get_job(self, job_id: str) -> GenerationJob | None:
        return await self.refresh(job_id)
