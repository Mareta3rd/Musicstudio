
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from musicstudio.config import settings
from musicstudio.agents.registry import AgentRegistry
from musicstudio.agents.runtime import SpecialistRuntime
from musicstudio.assistant import GeminiAssistantProvider, OpenAIAssistantProvider
from musicstudio.guide import CreativeGuide, GuideSession
from musicstudio.models import GenerationJob, GenerationRequest, ProviderCapabilities
from pydantic import BaseModel, Field
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
agent_registry = AgentRegistry()


class AssistantRequest(BaseModel):
    agent_id: str = Field(min_length=1, max_length=100)
    prompt: str = Field(min_length=1, max_length=12000)


class AssistantResponse(BaseModel):
    text: str
    provider: str
    model: str


class GuideStartResponse(BaseModel):
    session_id: str
    question_id: str | None
    question: str | None
    purpose: str | None


class GuideAnswerRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    question_id: str = Field(min_length=1, max_length=100)
    answer: str = Field(min_length=1, max_length=4000)


class GuideAnswerResponse(BaseModel):
    session_id: str
    question_id: str | None
    question: str | None
    purpose: str | None
    complete: bool
    brief: str | None = None


def get_assistant_runtime() -> SpecialistRuntime:
    provider_name = settings.assistant_provider
    if provider_name == "auto":
        if os.getenv("GEMINI_API_KEY"):
            provider_name = "gemini"
        elif os.getenv("OPENAI_API_KEY"):
            provider_name = "openai"

    if provider_name == "openai":
        assistant = OpenAIAssistantProvider(model=settings.openai_model)
    elif provider_name == "gemini":
        assistant = GeminiAssistantProvider(model=settings.gemini_model)
    else:
        raise HTTPException(status_code=503, detail="No external assistant provider is enabled")
    return SpecialistRuntime(agent_registry, assistant)


guides: dict[str, GuideSession] = {}
creative_guide = CreativeGuide()

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


@app.get("/api/agents")
async def agents() -> list[dict]:
    return [
        {
            "id": agent.id,
            "role": agent.role,
            "description": agent.description,
            "capabilities": list(agent.capabilities),
            "default_cost": agent.default_cost.value,
            "requires_audio": agent.requires_audio,
        }
        for agent in agent_registry.all()
    ]


@app.post("/api/guide/start", response_model=GuideStartResponse)
async def guide_start() -> GuideStartResponse:
    import uuid

    session_id = str(uuid.uuid4())
    session = creative_guide.start()
    guides[session_id] = session
    question = creative_guide.next_question(session)
    return GuideStartResponse(
        session_id=session_id,
        question_id=question.id if question else None,
        question=question.text if question else None,
        purpose=question.purpose if question else None,
    )


@app.post("/api/guide/answer", response_model=GuideAnswerResponse)
async def guide_answer(request: GuideAnswerRequest) -> GuideAnswerResponse:
    session = guides.get(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Guide session not found")
    try:
        question = creative_guide.answer(session, request.question_id, request.answer)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if question is None:
        return GuideAnswerResponse(
            session_id=request.session_id,
            question_id=None,
            question=None,
            purpose=None,
            complete=True,
            brief=creative_guide.brief(session),
        )
    return GuideAnswerResponse(
        session_id=request.session_id,
        question_id=question.id,
        question=question.text,
        purpose=question.purpose,
        complete=False,
    )


@app.post("/api/assistant", response_model=AssistantResponse)
async def assistant(request: AssistantRequest) -> AssistantResponse:
    try:
        result = await get_assistant_runtime().ask(request.agent_id, request.prompt)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return AssistantResponse(text=result.text, provider=result.provider, model=result.model)


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
