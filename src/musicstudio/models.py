
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class GenerationRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    lyrics: str = Field(default="", max_length=12000)
    duration: float = Field(default=30.0, ge=10.0, le=600.0)
    bpm: int | None = Field(default=None, ge=30, le=300)
    key_scale: str = Field(default="", max_length=80)
    vocal_language: str = Field(default="en", max_length=20)
    batch_size: int = Field(default=1, ge=1, le=8)
    seed: int | None = None

    @field_validator("prompt")
    @classmethod
    def clean_prompt(cls, value: str) -> str:
        value = " ".join(value.strip().split())
        if not value:
            raise ValueError("prompt cannot be empty")
        return value


class GenerationJob(BaseModel):
    id: str
    provider: str
    provider_job_id: str | None = None
    status: JobStatus
    request: GenerationRequest
    title: str = "Untitled generation"
    audio_url: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProviderStatus(BaseModel):
    status: JobStatus
    audio_path: str | None = None
    title: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class ProviderCapabilities(BaseModel):
    name: str
    label: str
    local: bool
    features: list[str] = Field(default_factory=list)
