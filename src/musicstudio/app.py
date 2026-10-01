
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from musicstudio.config import settings
from musicstudio.models import GenerationJob, GenerationRequest, ProviderCapabilities
from musicstudio.orchestrator import MusicOrchestrator
from musicstudio.providers.ace_step import AceStepProvider
from musicstudio.providers.mock import MockProvider


BASE_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = BASE_DIR / "web"

if settings.provider == "ace-step":
    provider = AceStepProvider(settings.ace_step_url, settings.ace_step_token)
else:
    provider = MockProvider()

orchestrator = MusicOrchestrator(provider)

app = FastAPI(title="Musicstudio", version="0.1.0")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/", response_class=FileResponse)
async def index() -> Path:
    return WEB_DIR / "index.html"


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "provider": provider.name}


@app.get("/api/providers", response_model=list[ProviderCapabilities])
async def providers() -> list[ProviderCapabilities]:
    return [provider.capabilities]


@app.post("/api/generate", response_model=GenerationJob)
async def generate(request: GenerationRequest) -> GenerationJob:
    return await orchestrator.create_job(request)


@app.get("/api/jobs/{job_id}", response_model=GenerationJob)
async def get_job(job_id: str) -> GenerationJob:
    job = await orchestrator.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/api/jobs/{job_id}/audio")
async def get_audio(job_id: str) -> Response:
    job = await orchestrator.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if not hasattr(provider, "download_audio"):
        raise HTTPException(status_code=404, detail="Audio is not available")
    if not job.provider_job_id:
        raise HTTPException(status_code=409, detail="Provider job is missing")

    provider_status = await provider.status(job.provider_job_id)
    audio_path = provider_status.audio_path
    if not audio_path:
        raise HTTPException(status_code=409, detail="Audio is not ready")

    content, media_type = await provider.download_audio(audio_path)
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'inline; filename="musicstudio-{job.id}.mp3"'},
    )
