from __future__ import annotations

import json
import re
from dataclasses import dataclass

from musicstudio.prosody import analyse_lines


@dataclass(frozen=True)
class LyricLine:
    text: str
    syllables: int | None = None


@dataclass(frozen=True)
class LyricSection:
    name: str
    lines: tuple[LyricLine, ...]


@dataclass(frozen=True)
class LyricDraft:
    title: str
    language: str
    theme: str
    sections: tuple[LyricSection, ...]

    def all_lines(self) -> list[str]:
        return [line.text for section in self.sections for line in section.lines]


def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith('```'):
        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned, count=1, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*```$', '', cleaned, count=1)
    value = json.loads(cleaned)
    if not isinstance(value, dict):
        raise ValueError('Lyricist output must be an object')
    return value


def parse_lyric_draft(text: str) -> LyricDraft:
    data = _extract_json(text)
    title = str(data.get('title', 'Untitled')).strip()
    language = str(data.get('language', 'es')).strip().lower()
    theme = str(data.get('theme', '')).strip()
    sections: list[LyricSection] = []
    for raw_section in data.get('sections', []):
        if not isinstance(raw_section, dict):
            continue
        name = str(raw_section.get('name', 'Section')).strip()
        raw_lines = raw_section.get('lines', [])
        lines = tuple(LyricLine(str(item).strip()) for item in raw_lines if str(item).strip())
        if lines:
            sections.append(LyricSection(name, lines))
    if not sections:
        raise ValueError('Lyricist output requires sections with lines')
    return LyricDraft(title, language, theme, tuple(sections))


def lyric_prompt(objective: str, brief: str) -> tuple[str, str]:
    instructions = (
        'You are the Musicstudio Lyricist. Write poetry intended to be sung. '
        'Respect theme, emotional voice and section architecture. '
        'Prefer natural stress and meaning over forced rhyme. '
        'Return ONLY valid JSON with keys title, language, theme, sections. '
        'Each section has name and lines; each line is a string. '
        'Do not surround the JSON with commentary.'
    )
    prompt = f'OBJECTIVE:\n{objective}\n\nCREATIVE BRIEF:\n{brief}'
    return instructions, prompt


def evaluate_lyric_draft(draft: LyricDraft, target_language: str = 'es') -> dict:
    lines = draft.all_lines()
    analysis = analyse_lines(lines, target_language)
    syllable_counts = [int(item['syllables']) for item in analysis]
    rhyme_keys = [str(item['rhyme_key']) for item in analysis]
    variation = len(set(syllable_counts))
    rhyme_repetition = len(rhyme_keys) - len(set(rhyme_keys))
    return {
        'line_count': len(lines),
        'syllables': syllable_counts,
        'rhyme_keys': rhyme_keys,
        'syllable_variation': variation,
        'repeated_rhyme_keys': rhyme_repetition,
        'note': 'Heuristic prosody analysis; human/AI review is still required for synalepha, stress and singability.',
    }