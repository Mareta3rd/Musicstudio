from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CostClass(str, Enum):
    FREE_LOCAL = "FREE_LOCAL"
    FREE_REMOTE = "FREE_REMOTE"
    PAID_OPTIONAL = "PAID_OPTIONAL"
    HUMAN_REQUIRED = "HUMAN_REQUIRED"


@dataclass(frozen=True)
class AgentSpec:
    id: str
    role: str
    description: str
    capabilities: tuple[str, ...]
    default_cost: CostClass = CostClass.FREE_LOCAL
    requires_audio: bool = False


AGENTS: tuple[AgentSpec, ...] = (
    AgentSpec("producer", "Producer / Director", "Owns the creative objective and delegates work.", ("planning", "delegation", "acceptance")),
    AgentSpec("lyricist", "Lyricist", "Writes structured lyrics with musical constraints.", ("lyrics", "sections", "rhyme")),
    AgentSpec("prosody", "Poetry / Prosody Specialist", "Checks meter, syllables, stress, rhyme and singability.", ("meter", "syllables", "stress", "rhyme", "phonetics")),
    AgentSpec("composer", "Composer", "Develops melody, harmony, motifs and form.", ("melody", "harmony", "chords", "form")),
    AgentSpec("arranger", "Arranger", "Turns ideas into an instrument-by-instrument arrangement.", ("instrumentation", "layers", "dynamics", "transitions")),
    AgentSpec("sound", "Sound Designer", "Chooses or designs timbres, textures, samples and effects.", ("timbre", "samples", "synthesis", "effects")),
    AgentSpec("editor", "Audio Editor", "Applies non-destructive audio edits.", ("cut", "fade", "stretch", "pitch", "comping"), requires_audio=True),
    AgentSpec("reference", "Reference Analyst", "Measures supplied audio and extracts production descriptors.", ("bpm", "key", "structure", "spectral", "loudness"), requires_audio=True),
    AgentSpec("separation", "Stem Specialist", "Separates or reconstructs musical components.", ("stems", "vocals", "drums", "bass"), requires_audio=True),
    AgentSpec("mixer", "Mixing Engineer", "Diagnoses and improves balance, dynamics, space and masking.", ("gain", "eq", "compression", "pan", "automation"), requires_audio=True),
    AgentSpec("polisher", "Finish / Polish Engineer", "Finds subtle defects and applies final micro-corrections.", ("cleanup", "transitions", "timing", "noise", "micro-edits"), requires_audio=True),
    AgentSpec("mastering", "Mastering Engineer", "Creates delivery masters and quality reports.", ("loudness", "true-peak", "dynamics", "delivery"), requires_audio=True),
    AgentSpec("rights", "Rights / Provenance Guardian", "Tracks asset source and permitted operations.", ("provenance", "license", "source")),
    AgentSpec("librarian", "Librarian", "Organizes projects, versions and assets.", ("organization", "versioning", "metadata")),
    AgentSpec("cleanup", "Storage Manager", "Controls temporary work and trash lifecycle.", ("retention", "cleanup", "storage")),
    AgentSpec("qa", "QA Engineer", "Validates code, assets, renders and requested constraints.", ("tests", "validation", "comparison")),
    AgentSpec("researcher", "Researcher", "Finds models, tools and production techniques.", ("research", "tooling", "benchmarks")),
)


class AgentRegistry:
    def __init__(self, agents: tuple[AgentSpec, ...] = AGENTS) -> None:
        self._agents = {agent.id: agent for agent in agents}

    def all(self) -> list[AgentSpec]:
        return list(self._agents.values())

    def get(self, agent_id: str) -> AgentSpec | None:
        return self._agents.get(agent_id)

    def capable_of(self, capability: str) -> list[AgentSpec]:
        return [a for a in self._agents.values() if capability in a.capabilities]
