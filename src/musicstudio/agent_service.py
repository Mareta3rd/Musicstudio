from __future__ import annotations

from musicstudio.agents.registry import AgentRegistry
from musicstudio.agents.runtime import SpecialistRuntime
from musicstudio.agent_audit import build_agent_audit
from musicstudio.agent_loop import AgentEvaluation, run_agent_loop
from musicstudio.lyricist import evaluate_lyric_draft, lyric_prompt, parse_lyric_draft


SUPPORTED_EXECUTABLE_AGENTS = {'lyricist'}


class AgentService:
    def __init__(self, registry: AgentRegistry, runtime: SpecialistRuntime) -> None:
        self.registry = registry
        self.runtime = runtime

    async def run_task(self, agent_id: str, objective: str, project_brief: str, project_id: str | None = None):
        if agent_id not in SUPPORTED_EXECUTABLE_AGENTS:
            raise ValueError(f'Agent is registered but not yet executable: {agent_id}')

        instructions, prompt = lyric_prompt(objective, project_brief)

        async def executor(_iteration: int, previous):
            prior = '' if previous is None else f'\n\nPREVIOUS CANDIDATE:\n{previous}'
            result = await self.runtime.ask(agent_id, prompt + prior, extra_instructions=instructions)
            return result.text

        def evaluator(candidate: str, _iteration: int) -> AgentEvaluation:
            try:
                draft = parse_lyric_draft(candidate)
                analysis = evaluate_lyric_draft(draft, draft.language)
                if analysis['line_count'] >= 4:
                    return AgentEvaluation('accept', 'Structured lyric draft validated; prosody metrics recorded.')
                return AgentEvaluation('continue', 'Draft contains too few lyric lines.')
            except (ValueError, TypeError, Exception) as exc:
                return AgentEvaluation('human_review', f'Lyric candidate could not be validated: {exc}')

        loop = await _async_loop(executor, evaluator, max_iterations=3)
        audit = build_agent_audit(agent_id, project_id, project_brief, loop.iterations, loop.status)
        return loop, audit


async def _async_loop(executor, evaluator, *, max_iterations: int):
    from musicstudio.agent_loop import AgentIteration, AgentLoopResult

    history = []
    previous = None
    for iteration in range(1, max_iterations + 1):
        candidate = await executor(iteration, previous)
        evaluation = evaluator(candidate, iteration)
        history.append(AgentIteration(iteration, candidate, evaluation))
        if evaluation.decision == 'accept':
            return AgentLoopResult('accepted', candidate, tuple(history))
        if evaluation.decision == 'human_review':
            return AgentLoopResult('human_review', candidate, tuple(history))
        previous = candidate
    return AgentLoopResult('max_iterations', history[-1].candidate if history else None, tuple(history))