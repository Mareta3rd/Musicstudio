from __future__ import annotations

import re
import unicodedata


VOWELS = 'aeiouáéíóúü'


def normalize_word(word: str) -> str:
    value = unicodedata.normalize('NFD', word.lower())
    value = ''.join(char for char in value if unicodedata.category(char) != 'Mn')
    return re.sub(r'[^a-zñ]', '', value)


def estimate_syllables(word: str, language: str = 'es') -> int:
    cleaned = normalize_word(word)
    if not cleaned:
        return 0
    groups = re.findall(r'[aeiou]+', cleaned)
    count = len(groups)
    if language == 'es' and cleaned.endswith(('ia', 'ie', 'io', 'ua', 'ue', 'uo')) and count > 1:
        # Conservative estimate: many common Spanish diphthongs form one syllable.
        count -= 1
    return max(1, count)


def line_syllables(line: str, language: str = 'es') -> int:
    words = re.findall(r'[A-Za-zÁÉÍÓÚÜáéíóúüÑñ]+', line)
    return sum(estimate_syllables(word, language) for word in words)


def rhyme_key(line: str) -> str:
    words = re.findall(r'[A-Za-zÁÉÍÓÚÜáéíóúüÑñ]+', line.lower())
    if not words:
        return ''
    word = normalize_word(words[-1])
    if len(word) <= 3:
        return word
    # Assonant/consonant rhyme work better later; this is a transparent heuristic.
    return word[-3:]


def analyse_lines(lines: list[str], language: str = 'es') -> list[dict[str, object]]:
    return [
        {
            'line': line,
            'syllables': line_syllables(line, language),
            'rhyme_key': rhyme_key(line),
        }
        for line in lines
    ]