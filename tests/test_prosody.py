from musicstudio.prosody import analyse_lines, line_syllables, rhyme_key


def test_spanish_line_analysis_is_deterministic():
    assert line_syllables('La luna canta') == 5
    assert rhyme_key('camino') == 'ino'
    result = analyse_lines(['La luna canta', 'La noche levanta'])
    assert result[0]['syllables'] == 5
    assert result[0]['rhyme_key'] == 'nta'