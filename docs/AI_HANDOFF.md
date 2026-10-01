# AI HANDOFF — MUSICSTUDIO

## Current checkpoint

Repository: Mareta3rd/Musicstudio
Working branch: foundation/studio-core

Latest human-verified local baseline:
- Python 3.14.2
- Doctor: green
- Test suite: 10 passed
- 37 pytest-asyncio deprecation warnings
- OpenAI secret present in Codespaces, value not exposed

## Inherited mechanisms

Musicstudio adopts the most useful tested mechanisms from the Arsa & Pisha semantic architecture:

- branch synchronization as a first-class invariant;
- closed work blocks with one next direction;
- durable AI handoff documentation;
- bounded autonomous loops;
- immutable audit records;
- provider-neutral normalization;
- frozen execution boundaries;
- semantic regression detection;
- deterministic evaluators where possible;
- secrets confined to environment/secret storage;
- external providers treated as sources of observations or proposals, never as owners of canonical project state.

## Current Musicstudio architecture

- FastAPI control plane
- Mock and ACE-Step music providers
- OpenAI specialist provider (optional)
- release/album domain
- addon registry
- specialist-agent registry
- Codespaces runtime

## Standard resume command

    bash scripts/start_work_block.sh

This synchronizes the active branch, installs current development dependencies, runs Doctor, and executes the complete test suite.

## Primary next target

Synchronize the Codespace with the current remote checkpoint, verify the OpenAI specialist call, then persist the project/version graph.

## Known limitations

- ACE-Step is not yet running in the current Codespace.
- FFmpeg is optional and not installed.
- specialist agents are registered and routable, but autonomous multi-agent orchestration is not yet active.
- project persistence is not yet implemented.
