from musicstudio.agents.registry import AgentRegistry
from musicstudio.control_plane import MusicControlPlane
from musicstudio.library_store import LibraryStore
from musicstudio.project_store import ProjectStore
from musicstudio.task_store import TaskStore


def test_control_plane_reads_shared_project_state(tmp_path):
    db = tmp_path / 'musicstudio.db'
    projects = ProjectStore(db)
    library = LibraryStore(db)
    tasks = TaskStore(db)
    project = projects.create_project(title='Control Test')
    projects.save_state(project.id, {'tracks': [], 'mix': {'status': 'new'}})
    tasks.create_task(project.id, 'lyricist', 'Write a verse')

    plane = MusicControlPlane(projects, library, tasks, AgentRegistry())

    assert plane.inspect_project(project.id)['title'] == 'Control Test'
    assert plane.inspect_state(project.id)['mix']['status'] == 'new'
    assert len(plane.inspect_tasks(project.id)) == 1
    assert 'producer' in plane.specialist_ids()