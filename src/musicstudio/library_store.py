from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AssetRecord:
    id: str
    project_id: str | None
    name: str
    path: str
    kind: str
    state: str
    source: str
    license: str
    checksum: str | None
    expires_at: str | None
    created_at: str


class LibraryStore:
    def __init__(self, path: str | Path = 'data/musicstudio.db') -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
        return db

    def _init_db(self) -> None:
        with self._connect() as db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS assets (
                    id TEXT PRIMARY KEY,
                    project_id TEXT,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    state TEXT NOT NULL DEFAULT 'active',
                    source TEXT NOT NULL DEFAULT '',
                    license TEXT NOT NULL DEFAULT '',
                    checksum TEXT,
                    expires_at TEXT,
                    created_at TEXT NOT NULL
                )
            ''')

    def add_asset(
        self,
        *,
        name: str,
        path: str,
        kind: str,
        project_id: str | None = None,
        state: str = 'active',
        source: str = '',
        license: str = '',
        checksum: str | None = None,
        retention_days: int | None = None,
    ) -> AssetRecord:
        created = _now()
        expires_at = None
        if retention_days is not None:
            expires_at = (datetime.now(timezone.utc) + timedelta(days=max(0, retention_days))).isoformat()
        asset = AssetRecord(
            str(uuid4()), project_id, name.strip(), path, kind.strip(), state.strip(),
            source.strip(), license.strip(), checksum, expires_at, created,
        )
        with self._connect() as db:
            db.execute(
                'INSERT INTO assets (id,project_id,name,path,kind,state,source,license,checksum,expires_at,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (asset.id, asset.project_id, asset.name, asset.path, asset.kind, asset.state, asset.source, asset.license, asset.checksum, asset.expires_at, asset.created_at),
            )
        return asset

    def list_assets(self, project_id: str | None = None, state: str | None = None) -> list[AssetRecord]:
        query = 'SELECT * FROM assets WHERE 1=1'
        params: list[str] = []
        if project_id is not None:
            query += ' AND project_id = ?'
            params.append(project_id)
        if state is not None:
            query += ' AND state = ?'
            params.append(state)
        query += ' ORDER BY created_at DESC'
        with self._connect() as db:
            rows = db.execute(query, params).fetchall()
        return [self._row(row) for row in rows]

    def expired_temporary_assets(self, now: str | None = None) -> list[AssetRecord]:
        current = now or _now()
        with self._connect() as db:
            rows = db.execute(
                "SELECT * FROM assets WHERE state = 'temp' AND expires_at IS NOT NULL AND expires_at <= ? ORDER BY expires_at",
                (current,),
            ).fetchall()
        return [self._row(row) for row in rows]

    def move_state(self, asset_id: str, state: str) -> AssetRecord | None:
        with self._connect() as db:
            result = db.execute('UPDATE assets SET state = ? WHERE id = ?', (state, asset_id))
            if result.rowcount == 0:
                return None
        with self._connect() as db:
            row = db.execute('SELECT * FROM assets WHERE id = ?', (asset_id,)).fetchone()
        return self._row(row) if row else None

    @staticmethod
    def _row(row: sqlite3.Row) -> AssetRecord:
        return AssetRecord(
            row['id'], row['project_id'], row['name'], row['path'], row['kind'],
            row['state'], row['source'], row['license'], row['checksum'],
            row['expires_at'], row['created_at'],
        )