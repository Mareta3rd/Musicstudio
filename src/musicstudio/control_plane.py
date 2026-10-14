from __future__ import annotations

from dataclasses import dataclass

from musicstudio.agents.registry import AgentRegistry
from musicstudio.library_store import LibraryStore
from musicstudio.project_store import ProjectStore
from musicstudio.task_store import TaskStore


@dataclass
class MusicControlPlane:
    projects: ProjectStore
    library: LibraryStore
    tasks: TaskStore
    agents: AgentRegistry

    def inspect_project(self, project_id: str) -> dict:
        project = self.projects.get_project(project_id)
        if project is None:
            raise KeyError(f'Project not found: {project_id}')
        return project.__dict__

    def inspect_state(self, project_id: str) -> dict:
        self.inspect_project(project_id)
        return self.projects.get_state(project_id)

    def inspect_versions(self, project_id: str) -> list[dict]:
        self.inspect_project(project_id)
        return self.projects.list_versions(project_id)

    def inspect_tasks(self, project_id: str) -> list[dict]:
        self.inspect_project(project_id)
        return [task.__dict__ for task in self.tasks.list_tasks(project_id)]

    def inspect_assets(self, project_id: str | None = None) -> list[dict]:
        return [asset.__dict__ for asset in self.library.list_assets(project_id)]

    def specialist_ids(self) -> list[str]:
        return [agent.id for agent in self.agents.all()]
