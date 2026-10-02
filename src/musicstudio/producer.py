from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ProducerTask:
    agent_id: str
    objective: str
    acceptance: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProducerPlan:
    summary: str
    creative_direction: tuple[str, ...]
    tasks: tuple[ProducerTask, ...]


CORE_AGENT_ORDER = (
    'lyricist',
    'prosody',
    'composer',
    'arranger',
    'sound',
    'vocal',
    'editor',
    'mixer',
    'polisher',
    'mastering',
)


def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith('```'):
        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned, count=1, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*```$', '', cleaned, count=1)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError('Producer returned invalid JSON') from exc
    if not isinstance(value, dict):
        raise ValueError('Producer output must be an object')
    return value


def parse_producer_plan(text: str) -> ProducerPlan:
    data = _extract_json(text)
    summary = str(data.get('summary', '')).strip()
    if not summary:
        raise ValueError('Producer plan requires summary')
    direction = tuple(str(item).strip() for item in data.get('creative_direction', []) if str(item).strip())
    tasks: list[ProducerTask] = []
    for item in data.get('tasks', []):
        if not isinstance(item, dict):
            continue
        agent_id = str(item.get('agent_id', '')).strip()
        objective = str(item.get('objective', '')).strip()
        acceptance = tuple(str(value).strip() for value in item.get('acceptance', []) if str(value).strip())
        if agent_id and objective:
            tasks.append(ProducerTask(agent_id, objective, acceptance))
    if not tasks:
        raise ValueError('Producer plan requires at least one specialist task')
    return ProducerPlan(summary, direction, tuple(tasks))


def producer_prompt(creative_brief: str, project_context: str = '') -> tuple[str, str]:
    instructions = (
        'You are the Producer / Director of Musicstudio. '
        'Turn a creative brief into a concrete production plan. '
        'Do not write the full song. Delegate specialist work. '
        'Preserve the artistic intent. Keep the plan concise and actionable. '
        'Return ONLY valid JSON with keys: summary, creative_direction, tasks. '
        'Each task must contain agent_id, objective, acceptance.'
    )
    prompt = (
        'CREATIVE BRIEF:\n' + creative_brief + '\n\n' +
        'PROJECT CONTEXT:\n' + (project_context or 'None provided') + '\n\n' +
        'VALID SPECIALIST AGENTS:\n' + ', '.join(CORE_AGENT_ORDER)
    )
    return instructions, prompt