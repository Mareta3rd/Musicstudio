from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AgentTaskRecord:
    id: str
    project_id: str
    agent_id: str
    objective: str
    acceptance: tuple[str, ...]
    status: str
    result: dict | None
    created_at: str
    updated_at: str


class TaskStore:
    def __init__(self, path: str | Path = 'data/musicstudio.db') -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def _init_db(self) -> None:
        with self._connect() as db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS agent_tasks (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    objective TEXT NOT NULL,
                    acceptance TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'queued',
                    result TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')

    def create_task(self, project_id: str, agent_id: str, objective: str, acceptance: tuple[str, ...] = ()) -> AgentTaskRecord:
        now = _now()
        task = AgentTaskRecord(str(uuid4()), project_id, agent_id, objective, acceptance, 'queued', None, now, now)
        with self._connect() as db:
            db.execute(
                'INSERT INTO agent_tasks (id,project_id,agent_id,objective,acceptance,status,result,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?)',
                (task.id, task.project_id, task.agent_id, task.objective, json.dumps(list(task.acceptance), ensure_ascii=False), task.status, None, task.created_at, task.updated_at),
            )
        return task

    def list_tasks(self, project_id: str, status: str | None = None) -> list[AgentTaskRecord]:
        query = 'SELECT * FROM agent_tasks WHERE project_id = ?'
        params: list[str] = [project_id]
        if status is not None:
            query += ' AND status = ?'
            params.append(status)
        query += ' ORDER BY created_at ASC'
        with self._connect() as db:
            rows = db.execute(query, params).fetchall()
        return [self._row(row) for row in rows]

    def get_task(self, task_id: str) -> AgentTaskRecord | None:
        with self._connect() as db:
            row = db.execute('SELECT * FROM agent_tasks WHERE id = ?', (task_id,)).fetchone()
        return self._row(row) if row else None

    def set_status(self, task_id: str, status: str, result: dict | None = None) -> AgentTaskRecord | None:
        now = _now()
        encoded = json.dumps(result, ensure_ascii=False, sort_keys=True) if result is not None else None
        with self._connect() as db:
            db.execute('UPDATE agent_tasks SET status = ?, result = ?, updated_at = ? WHERE id = ?', (status, encoded, now, task_id))
        return self.get_task(task_id)

    @staticmethod
    def _row(row: sqlite3.Row) -> AgentTaskRecord:
        result = json.loads(row['result']) if row['result'] else None
        return AgentTaskRecord(
            row['id'], row['project_id'], row['agent_id'], row['objective'],
            tuple(json.loads(row['acceptance'])), row['status'], result,
            row['created_at'], row['updated_at'],
        )