from __future__ import annotations

import os

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from musicstudio.config import settings
from musicstudio.agents.registry import AgentRegistry
from musicstudio.agents.runtime import SpecialistRuntime
from musicstudio.assistant import FallbackAssistantProvider, GeminiAssistantProvider, GroqAssistantProvider, OpenAIAssistantProvider
from musicstudio.guide import CreativeGuide, GuideSession
from musicstudio.producer import parse_producer_plan, producer_prompt
from musicstudio.project_store import ProjectStore
from musicstudio.release import ReleaseKind
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


class CreateProjectRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    artist: str = Field(default="", max_length=200)
    kind: ReleaseKind = ReleaseKind.ep
    concept: str = Field(default="", max_length=2000)
    creative_brief: str = Field(default="", max_length=16000)


class GuideCreateProjectRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    artist: str = Field(default="", max_length=200)
    kind: ReleaseKind = ReleaseKind.mini


class ProducerPlanRequest(BaseModel):
    project_id: str = Field(min_length=1, max_length=100)


class ProducerPlanResponse(BaseModel):
    project_id: str
    summary: str
    creative_direction: list[str]
    tasks: list[dict]
    version: int
    provider: str
    model: str


def get_assistant_runtime() -> SpecialistRuntime:
    provider_name = settings.assistant_provider

    if provider_name == "auto":
        free_providers = []
        if os.getenv("GEMINI_API_KEY"):
            free_providers.append(GeminiAssistantProvider(model=settings.gemini_model))
        if os.getenv("GROQ_API_KEY"):
            free_providers.append(GroqAssistantProvider(model=settings.groq_model))
        if not free_providers:
            raise HTTPException(status_code=503, detail="No free assistant provider is enabled")
        assistant = FallbackAssistantProvider(free_providers)
        return SpecialistRuntime(agent_registry, assistant)

    if provider_name == "openai":
        assistant = OpenAIAssistantProvider(model=settings.openai_model)
    elif provider_name == "gemini":
        assistant = GeminiAssistantProvider(model=settings.gemini_model)
    elif provider_name == "groq":
        assistant = GroqAssistantProvider(model=settings.groq_model)
    else:
        raise HTTPException(status_code=503, detail="No external assistant provider is enabled")
    return SpecialistRuntime(agent_registry, assistant)


guides: dict[str, GuideSession] = {}
creative_guide = CreativeGuide()
project_store = ProjectStore()

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


@app.get("/api/projects", response_model=list[dict])
async def list_projects() -> list[dict]:
    return [project.__dict__ for project in project_store.list_projects()]


@app.post("/api/projects", response_model=dict)
async def create_project(request: CreateProjectRequest) -> dict:
    project = project_store.create_project(
        title=request.title,
        artist=request.artist,
        kind=request.kind,
        concept=request.concept,
        creative_brief=request.creative_brief,
    )
    return project.__dict__


@app.get("/api/projects/{project_id}", response_model=dict)
async def get_project(project_id: str) -> dict:
    project = project_store.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.__dict__


@app.get("/api/projects/{project_id}/versions", response_model=list[dict])
async def get_project_versions(project_id: str) -> list[dict]:
    if project_store.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_store.list_versions(project_id)


@app.post("/api/guide/create-project", response_model=dict)
async def guide_create_project(request: GuideCreateProjectRequest) -> dict:
    session = guides.get(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Guide session not found")
    brief = creative_guide.brief(session)
    project = project_store.create_project(
        title=request.title,
        artist=request.artist,
        kind=request.kind,
        concept="",
        creative_brief=brief,
    )
    version = project_store.create_version(
        project.id,
        "Creative brief",
        {"type": "creative_brief", "brief": brief, "source": "guide"},
    )
    return {"project": project.__dict__, "version": version, "brief": brief}


@app.post("/api/projects/producer-plan", response_model=ProducerPlanResponse)
async def producer_plan(request: ProducerPlanRequest) -> ProducerPlanResponse:
    project = project_store.get_project(request.project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    instructions, prompt = producer_prompt(project.creative_brief, project.concept or project.kind)
    try:
        result = await get_assistant_runtime().ask("producer", prompt, extra_instructions=instructions)
        plan = parse_producer_plan(result.text)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    version = project_store.create_version(
        project.id,
        "Producer plan",
        {
            "type": "producer_plan",
            "summary": plan.summary,
            "creative_direction": list(plan.creative_direction),
            "tasks": [
                {
                    "agent_id": task.agent_id,
                    "objective": task.objective,
                    "acceptance": list(task.acceptance),
                }
                for task in plan.tasks
            ],
        },
    )
    return ProducerPlanResponse(
        project_id=project.id,
        summary=plan.summary,
        creative_direction=list(plan.creative_direction),
        tasks=[
            {
                "agent_id": task.agent_id,
                "objective": task.objective,
                "acceptance": list(task.acceptance),
            }
            for task in plan.tasks
        ],
        version=version,
        provider=result.provider,
        model=result.model,
    )


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
