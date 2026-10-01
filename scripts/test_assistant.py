from __future__ import annotations

import asyncio
import os

from musicstudio.assistant import OpenAIAssistantProvider


async def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        return 2

    provider = OpenAIAssistantProvider()
    result = await provider.generate(
        "You are a careful connectivity test. Answer in one sentence.",
        "Reply only: Musicstudio API connection works.",
    )
    print(result.text)
    print(f"provider={result.provider} model={result.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
