from fastapi.testclient import TestClient

import musicstudio.app as app_module
from musicstudio.assistant import AssistantResult
from musicstudio.guide import CreativeGuide
from musicstudio.library_store import LibraryStore
from musicstudio.project_store import ProjectStore
from musicstudio.task_store import TaskStore


class ProducerRuntimeStub:
    async def ask(self, agent_id, prompt, extra_instructions=""):
        assert agent_id == "producer"
        return AssistantResult(
            text='{"summary":"Nocturnal mini","creative_direction":["warm"],"tasks":['
                 '{"agent_id":"lyricist","objective":"Write lyrics","acceptance":["singable"]},'
                 '{"agent_id":"composer","objective":"Create motif","acceptance":["recurring"]}]}',
            model="test-model",
            provider="test",
        )


def test_guide_project_producer_plan_and_task_queue(tmp_path, monkeypatch):
    db = tmp_path / "musicstudio.db"
    monkeypatch.setattr(app_module, "project_store", ProjectStore(db))
    monkeypatch.setattr(app_module, "library_store", LibraryStore(db))
    monkeypatch.setattr(app_module, "task_store", TaskStore(db))
    monkeypatch.setattr(app_module, "creative_guide", CreativeGuide())
    monkeypatch.setattr(app_module, "guides", {})
    monkeypatch.setattr(app_module, "get_assistant_runtime", lambda: ProducerRuntimeStub())

    answers = [
        ("intent", "melancolía luminosa"),
        ("format", "mini de tres canciones"),
        ("world", "sintetizadores cálidos y percusión orgánica"),
        ("reference", "texturas analógicas, sin copiar melodías"),
        ("voice", "voz cercana e íntima"),
        ("energy", "crece gradualmente"),
        ("signature", "motivo recurrente de cuatro notas"),
        ("visual", "carretera nocturna ámbar y azul"),
        ("constraint", "evitar compresión excesiva"),
    ]

    with TestClient(app_module.app) as client:
        guide = client.post("/api/guide/start").json()
        for question_id, answer in answers:
            assert guide["question_id"] == question_id
            response = client.post("/api/guide/answer", json={
                "session_id": guide["session_id"],
                "question_id": question_id,
                "answer": answer,
            })
            assert response.status_code == 200
            guide = response.json()

        assert guide["complete"] is True
        created = client.post("/api/guide/create-project", json={
            "session_id": guide["session_id"],
            "title": "Viaje Nocturno",
            "artist": "Demo",
            "kind": "mini",
        })
        assert created.status_code == 200
        project_id = created.json()["project"]["id"]
        assert "emotional intent: melancolía luminosa" in created.json()["brief"]

        planned = client.post("/api/projects/producer-plan", json={"project_id": project_id})
        assert planned.status_code == 200
        assert len(planned.json()["tasks"]) == 2

        state = client.get(f"/api/projects/{project_id}/state").json()
        assert state["release"]["kind"] == "mini"
        assert state["creative_intent"]["intent"] == "melancolía luminosa"

        versions = client.get(f"/api/projects/{project_id}/versions").json()
        assert any(item["label"] == "Creative brief" for item in versions)
        assert any(item["label"] == "Producer plan" for item in versions)

        tasks = client.get(f"/api/projects/{project_id}/tasks").json()
        assert [item["agent_id"] for item in tasks] == ["lyricist", "composer"]
        assert all(item["status"] == "queued" for item in tasks)
        assert tasks[0]["executable"] is True
        assert tasks[1]["executable"] is False

        assert ProjectStore(db).get_project(project_id) is not None
        assert len(TaskStore(db).list_tasks(project_id)) == 2
