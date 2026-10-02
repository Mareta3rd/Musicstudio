from musicstudio.release import Release, ReleaseKind, ReleaseTrack, TrackRole


def test_release_preserves_album_order_and_duration():
    release = Release(
        title="Nocturno Mediterráneo",
        kind=ReleaseKind.mini,
        tracks=[
            ReleaseTrack(title="II", position=2, duration=182.5),
            ReleaseTrack(title="I", position=1, role=TrackRole.intro, duration=61),
            ReleaseTrack(title="III", position=3, role=TrackRole.outro, duration=204),
        ],
    )

    assert [track.title for track in release.ordered_tracks()] == ["I", "II", "III"]
    assert release.total_duration() == 447.5
    assert release.validate_positions()


def test_release_rejects_duplicate_positions():
    release = Release(
        title="Test",
        tracks=[
            ReleaseTrack(title="A", position=1),
            ReleaseTrack(title="B", position=1),
        ],
    )
    assert not release.validate_positions()
