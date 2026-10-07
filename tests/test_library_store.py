from musicstudio.library_store import LibraryStore


def test_library_tracks_provenance_and_state(tmp_path):
    store = LibraryStore(tmp_path / 'musicstudio.db')
    asset = store.add_asset(
        name='reference.mp3',
        path='/music/reference.mp3',
        kind='audio',
        source='user-owned',
        license='owned',
        state='reference',
    )
    loaded = store.list_assets(state='reference')
    assert loaded[0].id == asset.id
    assert loaded[0].source == 'user-owned'
    assert loaded[0].license == 'owned'


def test_temporary_assets_can_expire_without_being_deleted(tmp_path):
    store = LibraryStore(tmp_path / 'musicstudio.db')
    asset = store.add_asset(
        name='preview.wav',
        path='/tmp/preview.wav',
        kind='audio',
        state='temp',
        retention_days=0,
    )
    expired = store.expired_temporary_assets()
    assert [item.id for item in expired] == [asset.id]
    assert store.move_state(asset.id, 'trash').state == 'trash'