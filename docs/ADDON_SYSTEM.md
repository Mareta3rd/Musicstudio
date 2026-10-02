# Musicstudio — Addon System

## Goal

Musicstudio should be extensible without rewriting the core.

The addon layer is deliberately similar in spirit to a media-center plugin ecosystem:

- the core owns state, permissions and orchestration
- addons announce capabilities
- addons can provide providers, agents, analyzers, effects, importers, exporters, library connectors or UI
- addons are optional

The guiding rule is:

core first, capability second, dependency last.

## Addon manifest

Each addon declares:

- id
- name
- version
- type
- capabilities
- entrypoint
- network requirement
- cost class
- configuration schema

## Addon types

provider / agent / analyzer / effect / importer / exporter / library / ui

## Trust

An addon is executable software.

Installing an addon therefore becomes an explicit trust decision.

The Studio should display source, version, permissions, network access, file access, cost class and license where supplied.

## Zero-cost policy

Paid providers never activate silently.

The default selector remains:

FREE_LOCAL -> FREE_REMOTE -> PAID_OPTIONAL -> HUMAN_REQUIRED

## Future catalog

A future addon catalog can install AI providers, sound libraries, notation tools, visualization engines, DAW bridges, MIDI tools, mastering chains, video generators and artwork generators.

No catalog dependency is required for the core Studio.
