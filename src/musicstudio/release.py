from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class ReleaseKind(str, Enum):
    single = "single"
    mini = "mini"
    ep = "ep"
    lp = "lp"
    live = "live"
    unplugged = "unplugged"
    soundtrack = "soundtrack"


class TrackRole(str, Enum):
    intro = "intro"
    interlude = "interlude"
    main = "main"
    transition = "transition"
    outro = "outro"
    bonus = "bonus"


class ArtworkPackage(BaseModel):
    cover: str | None = None
    back_cover: str | None = None
    booklet: str | None = None
    lyrics_sheet: str | None = None
    visualizer: str | None = None
    video: str | None = None


class ReleaseTrack(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    role: TrackRole = TrackRole.main
    project_id: str | None = None
    position: int = Field(ge=1)
    duration: float | None = Field(default=None, ge=0)
    notes: str = ""
    tags: list[str] = Field(default_factory=list)
    transition_in: str | None = None
    transition_out: str | None = None


class Release(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    artist: str = ""
    kind: ReleaseKind = ReleaseKind.ep
    concept: str = ""
    narrative: str = ""
    style: str = ""
    tracks: list[ReleaseTrack] = Field(default_factory=list)
    artwork: ArtworkPackage = Field(default_factory=ArtworkPackage)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def ordered_tracks(self) -> list[ReleaseTrack]:
        return sorted(self.tracks, key=lambda track: track.position)

    def total_duration(self) -> float:
        return round(sum(track.duration or 0 for track in self.tracks), 3)

    def add_track(self, track: ReleaseTrack) -> None:
        self.tracks.append(track)

    def validate_positions(self) -> bool:
        positions = [track.position for track in self.tracks]
        return len(positions) == len(set(positions)) and all(p >= 1 for p in positions)
