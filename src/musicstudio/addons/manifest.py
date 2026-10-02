from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AddonType(str, Enum):
    provider = "provider"
    agent = "agent"
    analyzer = "analyzer"
    effect = "effect"
    importer = "importer"
    exporter = "exporter"
    library = "library"
    ui = "ui"


class AddonManifest(BaseModel):
    id: str = Field(min_length=1, max_length=100)
    name: str
    version: str
    type: AddonType
    description: str = ""
    capabilities: list[str] = Field(default_factory=list)
    entrypoint: str | None = None
    configurable: bool = False
    requires_network: bool = False
    cost_class: str = "FREE_LOCAL"
    settings_schema: dict[str, Any] = Field(default_factory=dict)


class AddonRegistry:
    def __init__(self) -> None:
        self._items: dict[str, AddonManifest] = {}

    def register(self, manifest: AddonManifest) -> None:
        if manifest.id in self._items:
            raise ValueError(f"Addon already registered: {manifest.id}")
        self._items[manifest.id] = manifest

    def get(self, addon_id: str) -> AddonManifest | None:
        return self._items.get(addon_id)

    def all(self) -> list[AddonManifest]:
        return list(self._items.values())

    def by_type(self, addon_type: AddonType) -> list[AddonManifest]:
        return [item for item in self._items.values() if item.type == addon_type]
