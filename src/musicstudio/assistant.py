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