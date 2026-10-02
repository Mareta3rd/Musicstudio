from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from musicstudio.release import Release, ReleaseKind, ReleaseTrack, ArtworkPackage


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ProjectRecord:
    id: str
    title: str
    artist: str
    kind: str
    concept: str
    creative_brief: str
    created_at: str
    updated_at: str


class ProjectStore:
    def __init__(self, path: str | Path = 'data/musicstudio.db') -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_db(self) -> None:
        with self._connect() as db:
            db.execute('PRAGMA foreign_keys = ON')
            db.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL DEFAULT '',
                    kind TEXT NOT NULL DEFAULT 'ep',
                    concept TEXT NOT NULL DEFAULT '',
                    creative_brief TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            db.execute('''
                CREATE TABLE IF NOT EXISTS versions (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    number INTEGER NOT NULL,
                    label TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(project_id, number)
                )
            ''')

    def create_project(
        self,
        *,
        title: str,
        artist: str = '',
        kind: ReleaseKind = ReleaseKind.ep,
        concept: str = '',
        creative_brief: str = '',
    ) -> ProjectRecord:
        project_id = str(uuid4())
        now = _now()
        with self._connect() as db:
            db.execute(
                'INSERT INTO projects (id,title,artist,kind,concept,creative_brief,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)',
                (project_id, title.strip(), artist.strip(), kind.value, concept.strip(), creative_brief.strip(), now, now),
            )
        return ProjectRecord(project_id, title.strip(), artist.strip(), kind.value, concept.strip(), creative_brief.strip(), now, now)

    def list_projects(self, limit: int = 100) -> list[ProjectRecord]:
        limit = max(1, min(int(limit), 500))
        with self._connect() as db:
            rows = db.execute(
                'SELECT * FROM projects ORDER BY updated_at DESC LIMIT ?',
                (limit,),
            ).fetchall()
        return [
            ProjectRecord(
                row['id'], row['title'], row['artist'], row['kind'],
                row['concept'], row['creative_brief'], row['created_at'], row['updated_at'],
            )
            for row in rows
        ]

    def get_project(self, project_id: str) -> ProjectRecord | None:
        with self._connect() as db:
            row = db.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
        if row is None:
            return None
        return ProjectRecord(
            row['id'], row['title'], row['artist'], row['kind'],
            row['concept'], row['creative_brief'], row['created_at'], row['updated_at'],
        )

    def save_brief(self, project_id: str, creative_brief: str) -> ProjectRecord | None:
        now = _now()
        with self._connect() as db:
            cursor = db.execute(
                'UPDATE projects SET creative_brief = ?, updated_at = ? WHERE id = ?',
                (creative_brief.strip(), now, project_id),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_project(project_id)

    def create_version(self, project_id: str, label: str, payload: dict) -> int:
        now = _now()
        with self._connect() as db:
            exists = db.execute('SELECT 1 FROM projects WHERE id = ?', (project_id,)).fetchone()
            if exists is None:
                raise KeyError(f'Project not found: {project_id}')
            row = db.execute('SELECT COALESCE(MAX(number), 0) AS maximum FROM versions WHERE project_id = ?', (project_id,)).fetchone()
            number = int(row['maximum']) + 1
            db.execute(
                'INSERT INTO versions (id,project_id,number,label,payload,created_at) VALUES (?,?,?,?,?,?)',
                (str(uuid4()), project_id, number, label, json.dumps(payload, ensure_ascii=False, sort_keys=True), now),
            )
            db.execute('UPDATE projects SET updated_at = ? WHERE id = ?', (now, project_id))
        return number

    def list_versions(self, project_id: str) -> list[dict]:
        with self._connect() as db:
            rows = db.execute('SELECT id, number, label, payload, created_at FROM versions WHERE project_id = ? ORDER BY number DESC', (project_id,)).fetchall()
        return [
            {
                'id': row['id'],
                'number': row['number'],
                'label': row['label'],
                'payload': json.loads(row['payload']),
                'created_at': row['created_at'],
            }
            for row in rows
        ]

    def create_release_project(self, release: Release, creative_brief: str = '') -> ProjectRecord:
        return self.create_project(
            title=release.title,
            artist=release.artist,
            kind=release.kind,
            concept=release.concept,
            creative_brief=creative_brief,
        )