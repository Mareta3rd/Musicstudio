import pytest

from musicstudio.agent_loop import AgentEvaluation, run_agent_loop


def test_agent_loop_stops_on_accept():
    seen = []

    def executor(iteration, previous):
        seen.append(previous)
        return iteration

    def evaluator(candidate, iteration):
        return AgentEvaluation('accept', 'good')

    result = run_agent_loop(executor, evaluator)
    assert result.status == 'accepted'
    assert result.candidate == 1
    assert len(result.iterations) == 1


def test_agent_loop_is_bounded():
    result = run_agent_loop(
        lambda iteration, previous: iteration,
        lambda candidate, iteration: AgentEvaluation('continue', 'refine'),
        max_iterations=2,
    )
    assert result.status == 'max_iterations'
    assert len(result.iterations) == 2


def test_agent_loop_rejects_invalid_limit():
    with pytest.raises(ValueError):
        run_agent_loop(lambda *_: 1, lambda *_: AgentEvaluation('accept', 'ok'), max_iterations=0)