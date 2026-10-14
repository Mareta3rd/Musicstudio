import pytest

from musicstudio.lyricist import evaluate_lyric_draft, parse_lyric_draft


def test_parse_lyric_draft_from_json():
    draft = parse_lyric_draft('{"title":"Viaje","language":"es","theme":"noche","sections":[{"name":"Verso","lines":["La noche gira","mi sombra camina","la ciudad respira","y el miedo termina"]}]}')
    assert draft.title == 'Viaje'
    assert len(draft.all_lines()) == 4


def test_lyric_evaluation_returns_measurements():
    draft = parse_lyric_draft('{"title":"Viaje","language":"es","theme":"noche","sections":[{"name":"Verso","lines":["La noche gira","mi sombra camina","la ciudad respira","y el miedo termina"]}]}')
    analysis = evaluate_lyric_draft(draft)
    assert analysis['line_count'] == 4
    assert len(analysis['syllables']) == 4


def test_bad_lyric_payload_is_rejected():
    with pytest.raises(ValueError):
        parse_lyric_draft('{"title":"Empty"}')