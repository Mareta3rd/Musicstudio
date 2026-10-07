import pytest

from musicstudio.timeline import Timeline, TimelineClip, TimelineSection, TimelineTrack


def test_timeline_orders_tracks_and_clips():
    bass = TimelineTrack(name='Bass', position=2)
    drums = TimelineTrack(name='Drums', position=1)
    timeline = Timeline(tracks=[bass, drums])
    timeline.clips.extend([
        TimelineClip(track_id=bass.id, start=4, duration=2),
        TimelineClip(track_id=bass.id, start=0, duration=4),
    ])
    assert [track.name for track in timeline.ordered_tracks()] == ['Drums', 'Bass']
    assert [clip.start for clip in timeline.clips_for_track(bass.id)] == [0, 4]


def test_timeline_detects_same_track_overlap():
    track = TimelineTrack(name='Vocal', position=1)
    timeline = Timeline(
        tracks=[track],
        clips=[
            TimelineClip(track_id=track.id, start=0, duration=3),
            TimelineClip(track_id=track.id, start=2.5, duration=1),
        ],
    )
    assert not timeline.validate_track_clip_overlaps()


def test_section_requires_positive_range():
    with pytest.raises(ValueError):
        TimelineSection(name='Verse', start=4, end=4)