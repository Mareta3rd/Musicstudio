from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    provider: str = os.getenv("MUSICSTUDIO_PROVIDER", "mock").strip().lower()
    assistant_provider: str = os.getenv("MUSICSTUDIO_ASSISTANT_PROVIDER", "auto").strip().lower()
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-6-luna").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.7-flash").strip()
    groq_model: str = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b").strip()
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openrouter/free").strip()
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b").strip()
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1").strip().rstrip("/")
    ace_step_url: str = os.getenv("ACE_STEP_URL", "http://127.0.0.1:8001").rstrip("/")
    ace_step_token: str = os.getenv("ACE_STEP_TOKEN", "")
    host: str = os.getenv("MUSICSTUDIO_HOST", "127.0.0.1")
    port: int = int(os.getenv("MUSICSTUDIO_PORT", "8000"))


settings = Settings()