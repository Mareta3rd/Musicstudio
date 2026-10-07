# Musicstudio — Control Plane

Musicstudio exposes one canonical control surface for every client and assistant.

## Core object

MusicControlPlane is independent of FastAPI and the browser.

It can be used by:
- web UI
- desktop shell
- CLI
- worker scheduler
- MCP server
- future external assistants

## Read operations

- inspect_project
- inspect_state
- inspect_versions
- inspect_tasks
- inspect_assets
- specialist_ids

## Mutation boundary

Mutations must remain explicit and versioned.

Future MCP tools should call ControlPlane methods instead of bypassing them.

## MCP implementation note

The current official Python MCP SDK is v2 and implements the 2026-07-28 MCP revision. The SDK project currently has published security advisories, including high-severity issues around HTTP/authentication behavior. Musicstudio therefore keeps the MCP contract documented but postpones adding the SDK as a hard dependency until its security posture is reviewed.

The first transport target should be local stdio. Remote Streamable HTTP comes later, with authentication and origin validation.

## Security

Read-only tools can expose broader project metadata.

Mutation tools must receive project/version scope, operation, inputs, expected output, cost class and confirmation policy.

Remote workers receive task-scoped data only.