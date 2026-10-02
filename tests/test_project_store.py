from musicstudio.project_store import ProjectStore
from musicstudio.release import Release, ReleaseKind


def test_project_and_versions_are_persistent(tmp_path):
    db = tmp_path / 'musicstudio.db'
    store = ProjectStore(db)
    project = store.create_project(title='Viaje Nocturno', kind=ReleaseKind.mini)
    store.create_version(project.id, 'Initial brief', {'brief': 'A nocturnal journey'})
    store.create_version(project.id, 'Producer plan', {'tasks': ['lyrics', 'composition']})

    reopened = ProjectStore(db)
    loaded = reopened.get_project(project.id)
    versions = reopened.list_versions(project.id)

    assert loaded is not None
    assert loaded.title == 'Viaje Nocturno'
    assert [v['number'] for v in versions] == [2, 1]


def test_release_can_seed_a_project(tmp_path):
    store = ProjectStore(tmp_path / 'musicstudio.db')
    release = Release(title='Tres Estaciones', kind=ReleaseKind.mini, artist='Demo')
    project = store.create_release_project(release, 'brief')
    assert project.title == 'Tres Estaciones'
    assert project.kind == 'mini'