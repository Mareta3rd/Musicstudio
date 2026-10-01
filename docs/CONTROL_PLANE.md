# Musicstudio — Control Plane

## Purpose

Musicstudio exposes one canonical control surface for browsers, desktop clients, CLI tools, workers and optional AI assistants.

The control plane is intentionally separate from the user interface and from any single model vendor.

## Operations

First-class operations should eventually include:

- inspect_project
- inspect_release
- inspect_track
- inspect_audio
- create_generation
- create_version
- analyze_reference
- propose_change
- apply_change
- compare_versions
- render_preview
- render_mix
- render_master
- export_delivery
- list_assets
- inspect_provenance
- list_workers
- schedule_task
- inspect_task

## MCP

An MCP server can expose a safe subset of these operations to compatible assistants.

Read operations should be separated from mutating operations.

Mutating operations should carry:

- project/version id
- requested operation
- input assets
- scope
- expected output
- provenance
- whether a new version is required
- cost class
- confirmation policy

## ChatGPT / Apps SDK

OpenAI's current Apps SDK is built on MCP and can package an application whose logic and UI connect to an existing backend.

Musicstudio can therefore have an optional ChatGPT-facing application later, while the core application remains independently usable.

OpenAI API usage is optional and must not be assumed to be covered by a ChatGPT subscription.

## Agent interaction

The Producer can use the same control plane as an external assistant:

assistant -> control plane -> project state -> specialist -> operation -> new version -> QA

## Security model

Every control request must be attributable to a caller and scoped to a project.

Remote workers never receive unrestricted access to the whole library.

By default:

- read-only tools are broader
- file transforms are scoped
- destructive operations create a version
- provenance-sensitive operations require explicit confirmation
- paid providers require explicit opt-in

## Transport independence

Initial implementation:

- local HTTP API
- CLI
- browser

Future:

- MCP server
- desktop bridge
- remote worker RPC
- optional WebSocket event stream

The project API remains the canonical contract.
