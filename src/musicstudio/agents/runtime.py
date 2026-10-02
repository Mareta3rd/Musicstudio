from __future__ import annotations

from musicstudio.agents.registry import AgentRegistry, AgentSpec


def specialist_instructions(agent: AgentSpec) -> str:
    capabilities = ", ".join(agent.capabilities)
    return (
        f"You are the Musicstudio {agent.role}. "
        f"Your responsibility: {agent.description} "
        f"Core capabilities: {capabilities}. "
        "Work as a specialist inside a larger production team. "
        "Do not pretend to have heard audio you were not given. "
        "Separate observations from proposals and never hide uncertainty. "
        "Prefer concrete, reversible actions and preserve the project's creative intent."
    )


class SpecialistRuntime:
    def __init__(self, registry: AgentRegistry, provider) -> None:
        self.registry = registry
        self.provider = provider

    async def ask(self, agent_id: str, prompt: str, extra_instructions: str = ""):
        agent = self.registry.get(agent_id)
        if agent is None:
            raise KeyError(f"Unknown agent: {agent_id}")
        instructions = specialist_instructions(agent)
        if extra_instructions.strip():
            instructions += " " + extra_instructions.strip()
        return await self.provider.generate(instructions, prompt)
