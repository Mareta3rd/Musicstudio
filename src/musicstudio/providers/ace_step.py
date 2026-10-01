
from __future__ import annotations

import json
from typing import Any

import httpx

from musicstudio.models import (
    GenerationRequest,
    JobStatus,
    ProviderCapabilities,
    ProviderStatus,
)
from musicstudio.providers.base import MusicProvider


class AceStepProvider(MusicProvider):
    name = "ace-step"
    capabilities = ProviderCapabilities(
        name="ace-step",
        label="ACE-Step 1.5",
        local=True,
        features=[
            "text-to-music",
            "lyrics",
            "reference audio",
            "repaint",
            "cover/remix",
            "stems",
            "multi-track",
            "metadata control",
        ],
    )

    def __init__(self, base_url: str, token: str = "") -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _headers(self) -> dict[str, str]:
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    async def submit(self, request: GenerationRequest) -> str:
        payload: dict[str, Any] = {
            "prompt": request.prompt,
            "lyrics": request.lyrics,
            "thinking": True,
            "vocal_language": request.vocal_language,
            "audio_format": "mp3",
            "audio_duration": request.duration,
            "batch_size": request.batch_size,
            "use_random_seed": request.seed is None,
        }
        if request.bpm is not None:
            payload["bpm"] = request.bpm
        if request.key_scale:
            payload["key_scale"] = request.key_scale
        if request.seed is not None:
            payload["seed"] = request.seed

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/release_task",
                json=payload,
                headers=self._headers(),
            )
            response.raise_for_status()
            body = response.json()

        if body.get("code") not in (None, 200):
            raise RuntimeError(body.get("error") or "ACE-Step rejected the request")

        data = body.get("data") or {}
        task_id = data.get("task_id")
        if not task_id:
            raise RuntimeError(f"ACE-Step response did not contain task_id: {body}")
        return str(task_id)

    async def status(self, provider_job_id: str) -> ProviderStatus:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/query_result",
                json={"task_id_list": [provider_job_id]},
                headers=self._headers(),
            )
            response.raise_for_status()
            body = response.json()

        if body.get("code") not in (None, 200):
            return ProviderStatus(
                status=JobStatus.failed,
                error=body.get("error") or "ACE-Step query failed",
            )

        data = body.get("data") or []
        if not data:
            return ProviderStatus(status=JobStatus.queued)

        item = data[0] or {}
        raw_status = int(item.get("status", 0))
        if raw_status == 0:
            return ProviderStatus(status=JobStatus.running)
        if raw_status == 2:
            return ProviderStatus(
                status=JobStatus.failed,
                error=item.get("error") or "ACE-Step generation failed",
            )

        result = item.get("result")
        results: list[dict[str, Any]] = []
        if isinstance(result, str) and result.strip():
            try:
                decoded = json.loads(result)
                results = decoded if isinstance(decoded, list) else [decoded]
            except json.JSONDecodeError:
                results = []

        first = results[0] if results else {}
        metas = first.get("metas") or {}
        audio_path = first.get("file")

        return ProviderStatus(
            status=JobStatus.completed,
            title=(first.get("prompt") or "ACE-Step generation")[:80],
            audio_path=audio_path,
            metadata={
                "duration": metas.get("duration"),
                "bpm": metas.get("bpm"),
                "key_scale": metas.get("keyscale"),
                "time_signature": metas.get("timesignature"),
                "seed": first.get("seed_value"),
                "lm_model": first.get("lm_model"),
                "dit_model": first.get("dit_model"),
            },
        )

    async def download_audio(self, audio_path: str) -> tuple[bytes, str]:
        if audio_path.startswith("http://") or audio_path.startswith("https://"):
            url = audio_path
        else:
            url = f"{self.base_url}{audio_path}"

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.get(url, headers=self._headers())
            response.raise_for_status()
            return response.content, response.headers.get("content-type", "audio/mpeg")
