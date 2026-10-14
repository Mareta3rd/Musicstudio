import pytest

from musicstudio.producer import parse_producer_plan, producer_prompt


def test_producer_plan_parser_accepts_fenced_json():
    plan = parse_producer_plan('''```json\n{"summary":"Build a nocturnal mini","creative_direction":["warm","slow burn"],"tasks":[{"agent_id":"lyricist","objective":"Write the lyric concept","acceptance":["clear theme"]},{"agent_id":"composer","objective":"Develop motif","acceptance":["reusable motif"]}]}\n```''')
    assert plan.summary == 'Build a nocturnal mini'
    assert plan.tasks[0].agent_id == 'lyricist'
    assert len(plan.tasks) == 2


def test_producer_plan_requires_tasks():
    with pytest.raises(ValueError):
        parse_producer_plan('{"summary":"No tasks"}')


def test_producer_prompt_is_explicit_about_json_and_delegation():
    instructions, prompt = producer_prompt('Melancolía luminosa', 'mini de tres temas')
    assert 'ONLY valid JSON' in instructions
    assert 'lyricist' in prompt