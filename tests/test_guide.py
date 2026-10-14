import pytest

from musicstudio.guide import CreativeGuide


def test_guide_asks_one_question_at_a_time():
    guide = CreativeGuide()
    session = guide.start()
    question = guide.next_question(session)
    assert question is not None
    assert question.id == "intent"


def test_guide_advances_without_reasking_answered_questions():
    guide = CreativeGuide()
    session = guide.start()
    guide.answer(session, "intent", "Quiero una sensación de viaje nocturno")
    question = guide.next_question(session)
    assert question is not None
    assert question.id == "format"


def test_guide_builds_a_compact_brief():
    guide = CreativeGuide()
    session = guide.start()
    guide.answer(session, "intent", "melancolía luminosa")
    guide.answer(session, "format", "mini de tres canciones")
    brief = guide.brief(session)
    assert "emotional intent: melancolía luminosa" in brief
    assert "release format: mini de tres canciones" in brief


def test_empty_answer_is_rejected():
    guide = CreativeGuide()
    session = guide.start()
    with pytest.raises(ValueError):
        guide.answer(session, "intent", "  ")