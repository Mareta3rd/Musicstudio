from __future__ import annotations

from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class ClipKind(str, Enum):
    audio = 'audio'
    midi = 'midi'
    automation = 'automation'
    marker = 'marker'


class TimelineSection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    notes: str = ''

    @model_validator(mode='after')
    def validate_range(self) -> 'TimelineSection':
        if self.end <= self.start:
            raise ValueError('section end must be greater than start')
        return self


class TimelineClip(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    track_id: str
    asset_id: str | None = None
    kind: ClipKind = ClipKind.audio
    start: float = Field(ge=0)
    duration: float = Field(gt=0)
    source_offset: float = Field(default=0, ge=0)
    gain_db: float = 0
    pan: float = Field(default=0, ge=-1, le=1)
    muted: bool = False
    notes: str = ''


class TimelineTrack(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    kind: str = 'audio'
    position: int = Field(ge=1)
    volume_db: float = 0
    pan: float = Field(default=0, ge=-1, le=1)
    muted: bool = False
    solo: bool = False


class Timeline(BaseModel):
    tempo: int | None = Field(default=None, ge=30, le=300)
    time_signature: str = '4/4'
    duration: float = Field(default=0, ge=0)
    tracks: list[TimelineTrack] = Field(default_factory=list)
    clips: list[TimelineClip] = Field(default_factory=list)
    sections: list[TimelineSection] = Field(default_factory=list)

    def ordered_tracks(self) -> list[TimelineTrack]:
        return sorted(self.tracks, key=lambda track: track.position)

    def clips_for_track(self, track_id: str) -> list[TimelineClip]:
        return sorted((clip for clip in self.clips if clip.track_id == track_id), key=lambda clip: clip.start)

    def validate_track_clip_overlaps(self) -> bool:
        for track in self.tracks:
            clips = self.clips_for_track(track.id)
            previous_end = 0.0
            for clip in clips:
                if clip.start < previous_end:
                    return False
                previous_end = clip.start + clip.duration
        return True