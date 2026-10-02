from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AssistantResult:
    text: str
    model: str
    provider: str


class AssistantProvider:
    name = "none"

    async def generate(self, instructions: str, prompt: str) -> AssistantResult:
        raise RuntimeError("No assistant provider is configured")


class OpenAIAssistantProvider(AssistantProvider):
    name = "openai"

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-6-luna")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

    async def generate(self, instructions: str, prompt: str) -> AssistantResult:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)
        try:
            response = await client.responses.create(model=self.model, instructions=instructions, input=prompt)
            return AssistantResult(text=response.output_text, model=self.model, provider=self.name)
        finally:
            await client.close()


class GeminiAssistantProvider(AssistantProvider):
    name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.7-flash")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

    async def generate(self, instructions: str, prompt: str) -> AssistantResult:
        from google import genai

        client = genai.Client(api_key=self.api_key)
        response = await client.aio.models.generate_content(
            model=self.model,
            contents=f"{instructions}\n\n{prompt}",
        )
        return AssistantResult(text=response.text or "", model=self.model, provider=self.name)

class GroqAssistantProvider(AssistantProvider):
    name = "groq"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str = "https://api.groq.com/openai/v1",
    ) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model or os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
        self.base_url = base_url.rstrip("/")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")

    async def generate(self, instructions: str, prompt: str) -> AssistantResult:
        import httpx

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
        }
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            if response.status_code >= 400:
                raise RuntimeError(f"Groq request failed ({response.status_code})")
            body = response.json()

        choices = body.get("choices") or []
        if not choices:
            raise RuntimeError("Groq returned no choices")
        message = choices[0].get("message") or {}
        text = message.get("content")
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("Groq returned empty content")
        return AssistantResult(text=text, model=self.model, provider=self.name)


class FallbackAssistantProvider(AssistantProvider):
    name = "auto-free"

    def __init__(self, providers: list[AssistantProvider]) -> None:
        self.providers = list(providers)

    async def generate(self, instructions: str, prompt: str) -> AssistantResult:
        if not self.providers:
            raise RuntimeError("No free assistant provider is configured")
        errors: list[str] = []
        for provider in self.providers:
            try:
                return await provider.generate(instructions, prompt)
            except Exception as exc:
                errors.append(f"{provider.name}: {exc}")
        raise RuntimeError("All configured free assistant providers failed: " + " | ".join(errors))


class OpenRouterAssistantProvider(AssistantProvider):
    name = "openrouter"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str = "https://openrouter.ai/api/v1",
    ) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.model = model or os.getenv("OPENROUTER_MODEL", "openrouter/free")
        self.base_url = base_url.rstrip("/")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured")

    async def generate(self, instructions: str, prompt: str) -> AssistantResult:
        import httpx

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
        }
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            if response.status_code >= 400:
                raise RuntimeError(f"OpenRouter request failed ({response.status_code})")
            body = response.json()

        choices = body.get("choices") or []
        if not choices:
            raise RuntimeError("OpenRouter returned no choices")
        message = choices[0].get("message") or {}
        text = message.get("content")
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("OpenRouter returned empty content")
        return AssistantResult(text=text, model=self.model, provider=self.name)
