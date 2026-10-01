
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    provider: str = os.getenv("MUSICSTUDIO_PROVIDER", "mock").strip().lower()
    ace_step_url: str = os.getenv("ACE_STEP_URL", "http://127.0.0.1:8001").rstrip("/")
    ace_step_token: str = os.getenv("ACE_STEP_TOKEN", "")
    host: str = os.getenv("MUSICSTUDIO_HOST", "127.0.0.1")
    port: int = int(os.getenv("MUSICSTUDIO_PORT", "8000"))


settings = Settings()
