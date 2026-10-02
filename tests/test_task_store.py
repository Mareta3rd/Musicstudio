from musicstudio.task_store import TaskStore


def test_task_lifecycle(tmp_path):
    store = TaskStore(tmp_path / 'musicstudio.db')
    task = store.create_task('p1', 'lyricist', 'Write verse', ('clear theme',))
    assert task.status == 'queued'
    assert store.list_tasks('p1')[0].id == task.id

    done = store.set_status(task.id, 'completed', {'draft': 'ok'})
    assert done is not None
    assert done.status == 'completed'
    assert done.result == {'draft': 'ok'}