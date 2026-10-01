import pytest

from musicstudio.agents.registry import AgentRegistry
from musicstudio.agents.runtime import SpecialistRuntime, specialist_instructions
from musicstudio.assistant import AssistantProvider


def test_specialist_instructions_include_role_and_capabilities():
    agent = AgentRegistry().get("prosody")
    assert agent is not None
    instructions = specialist_instructions(agent)
    assert "Prosody" in instructions
    assert "meter" in instructions


@pytest.mark.asyncio
async def test_missing_assistant_provider_fails_cleanly():
    class EmptyProvider(AssistantProvider):
        pass

    runtime = SpecialistRuntime(AgentRegistry(), EmptyProvider())
    with pytest.raises(RuntimeError):
        await runtime.ask("lyricist", "Write a verse")
