from __future__ import annotations

import asyncio
import os

from musicstudio.assistant import GeminiAssistantProvider, GroqAssistantProvider, OpenAIAssistantProvider


async def main() -> int:
    provider_name = os.getenv("MUSICSTUDIO_ASSISTANT_PROVIDER", "").strip().lower()
    if not provider_name:
        if os.getenv("GEMINI_API_KEY"):
            provider_name = "gemini"
        elif os.getenv("GROQ_API_KEY"):
            provider_name = "groq"
        else:
            provider_name = "openai"

    if provider_name == "gemini":
        provider = GeminiAssistantProvider()
    elif provider_name == "groq":
        provider = GroqAssistantProvider()
    elif provider_name == "openai":
        provider = OpenAIAssistantProvider()
    else:
        print(f"Unsupported assistant provider: {provider_name}")
        return 2

    result = await provider.generate(
        "You are a tiny connectivity test. Answer in one short sentence.",
        "Reply only: Musicstudio assistant connection works.",
    )
    print(result.text)
    print(f"provider={result.provider} model={result.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
