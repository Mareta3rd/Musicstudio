from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Literal, TypeVar

CandidateT = TypeVar('CandidateT')
Decision = Literal['continue', 'accept', 'human_review']
Status = Literal['accepted', 'human_review', 'max_iterations']


@dataclass(frozen=True)
class AgentEvaluation:
    decision: Decision
    reason: str


@dataclass(frozen=True)
class AgentIteration:
    iteration: int
    candidate: CandidateT
    evaluation: AgentEvaluation


@dataclass(frozen=True)
class AgentLoopResult(Generic[CandidateT]):
    status: Status
    candidate: CandidateT | None
    iterations: tuple[AgentIteration, ...]


Executor = Callable[[int, CandidateT | None], CandidateT]
Evaluator = Callable[[CandidateT, int], AgentEvaluation]


def run_agent_loop(
    executor: Executor[CandidateT],
    evaluator: Evaluator[CandidateT],
    *,
    max_iterations: int = 3,
    initial_candidate: CandidateT | None = None,
) -> AgentLoopResult[CandidateT]:
    if max_iterations < 1:
        raise ValueError('max_iterations must be at least 1')

    history: list[AgentIteration] = []
    previous = initial_candidate
    for iteration in range(1, max_iterations + 1):
        candidate = executor(iteration, previous)
        evaluation = evaluator(candidate, iteration)
        history.append(AgentIteration(iteration, candidate, evaluation))

        if evaluation.decision == 'accept':
            return AgentLoopResult('accepted', candidate, tuple(history))
        if evaluation.decision == 'human_review':
            return AgentLoopResult('human_review', candidate, tuple(history))
        if evaluation.decision != 'continue':
            raise ValueError(f'Unknown agent decision: {evaluation.decision!r}')
        previous = candidate

    candidate = history[-1].candidate if history else None
    return AgentLoopResult('max_iterations', candidate, tuple(history))