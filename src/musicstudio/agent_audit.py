from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Mapping

from musicstudio.agent_loop import AgentEvaluation, AgentIteration


def stable_fingerprint(value: Any) -> str:
    if isinstance(value, Mapping):
        text = '{' + ','.join(
            f'{stable_fingerprint(k)}:{stable_fingerprint(value[k])}'
            for k in sorted(value, key=lambda item: repr(item))
        ) + '}'
    elif isinstance(value, (list, tuple)):
        text = '[' + ','.join(stable_fingerprint(item) for item in value) + ']'
    else:
        text = repr(value)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


@dataclass(frozen=True)
class AgentAudit:
    agent_id: str
    project_id: str | None
    input_fingerprint: str
    iterations: tuple[dict[str, Any], ...]
    final_status: str
    final_reason: str | None


def build_agent_audit(
    agent_id: str,
    project_id: str | None,
    input_value: Any,
    iterations: tuple[AgentIteration[Any], ...],
    final_status: str,
) -> AgentAudit:
    final_reason = iterations[-1].evaluation.reason if iterations else None
    records = tuple(
        {
            'iteration': item.iteration,
            'candidate_fingerprint': stable_fingerprint(item.candidate),
            'decision': item.evaluation.decision,
            'reason': item.evaluation.reason,
        }
        for item in iterations
    )
    return AgentAudit(
        agent_id=agent_id,
        project_id=project_id,
        input_fingerprint=stable_fingerprint(input_value),
        iterations=records,
        final_status=final_status,
        final_reason=final_reason,
    )