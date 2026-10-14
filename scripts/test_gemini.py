from __future__ import annotations

import asyncio
import os

from musicstudio.assistant import GeminiAssistantProvider


async def main() -> int:
    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY is not set.")
        return 2
    provider = GeminiAssistantProvider()
    result = await provider.generate(
        "You are a tiny connectivity test. Answer in one short sentence.",
        "Reply only: Musicstudio Gemini connection works.",
    )
    print(result.text)
    print(f"provider={result.provider} model={result.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))