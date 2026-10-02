# AI HANDOFF — MUSICSTUDIO

## Current checkpoint

Repository: Mareta3rd/Musicstudio
Working branch: foundation/studio-core

Latest human-verified local baseline:
- Python 3.12.11
- Doctor: green
- Test suite: 16 passed before the current persistence/agent block
- Gemini assistant connectivity: VERIFIED
- OpenAI API connectivity: reached live API but account returned insufficient quota
- Gemini secret present in Codespaces, value not exposed
- Groq provider added but not yet live-verified

Remote development since that checkpoint has added project persistence, project state, asset catalog, Producer planning, bounded agent loops/audit, Creative Guide project creation UI, and free assistant fallback. These changes still require the next Codespace verification run.

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
- OpenAI specialist provider (optional; account currently has no API credits)
- Gemini specialist provider (free-tier candidate; live-verified)
- Groq/Qwen specialist provider (free-tier fallback; provider added)
- release/album domain
- addon registry
- specialist-agent registry
- Codespaces runtime

## Standard resume command

    bash scripts/start_work_block.sh

This synchronizes the active branch, installs current development dependencies, runs Doctor, and executes the complete test suite.

## Primary next target

Synchronize the Codespace with the current remote checkpoint, run the full suite, then exercise Guide -> persistent Project -> Producer plan.

## Known limitations

- ACE-Step is not yet running in the current Codespace.
- FFmpeg is optional and not installed.
- specialist agents are registered and routable, but autonomous multi-agent orchestration is not yet active.
- project persistence is implemented with SQLite; the new endpoints and persistence tests still need human Codespace execution.
- project state is stored as a generic JSON document separate from the SQL index.
- asset catalog/provenance/lifecycle persistence is implemented; physical cleanup is intentionally not automatic.
- Guide sessions remain in-memory until project creation; persistence starts once a project is created.
- Producer planning is implemented with validated JSON parsing and project-version storage; live execution of a Producer plan is still pending.
