# AI HANDOFF — MUSICSTUDIO

## Current checkpoint

Repository: Mareta3rd/Musicstudio
Working branch: foundation/studio-core
Current checkpoint: 9226eb0d15a597c9e323cf3bde65af922a417887

Latest repository CI before this block:
- Python 3.12: success
- Python 3.11: success
- checkpoint: 9709160d07e3baabb76ffc7c9c59504e7adb0116

Current work block:
- ACE-Step provider now accepts an optional httpx transport for deterministic integration testing.
- REST response code handling accepts numeric 200 and string "200".
- Added deterministic tests for release_task submission, query_result normalization, audio retrieval and failed-job normalization.
- The new checkpoint is being verified by GitHub CI on Python 3.11 and 3.12.
- Local container execution is unavailable because this environment cannot resolve github.com; no local test result is claimed for this block.

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
- OpenRouter free-model provider (opportunistic fallback; provider added)
- Ollama local provider (optional; provider added)
- release/album domain
- addon registry
- specialist-agent registry
- project/version/state persistence
- persistent specialist task queue
- bounded lyricist/prosody execution path
- Codespaces runtime

## Primary next target

After the current CI checkpoint is green, run the full Codespace work-block protocol and exercise the end-to-end control flow:
Guide -> persistent Project -> Producer plan -> queued tasks -> first live Lyricist task.

Then move directly into real ACE-Step verification:
release_task -> query_result -> audio retrieval -> Musicstudio audio proxy -> browser playback.

## Known limitations

- ACE-Step is not yet running in the current Codespace.
- FFmpeg is optional and not installed.
- specialist agents are registered and routable, but autonomous multi-agent orchestration is not yet active.
- live Gemini execution through the task endpoint still needs verification.
- timeline/arrangement domain model is implemented; route integration is intentionally deferred until the project state API settles.
- Control Plane abstraction is implemented; MCP server remains deferred pending SDK security review.
- OpenRouter free fallback is implemented; live connectivity is not verified.
- project state is stored as a generic JSON document separate from the SQL index.
- asset catalog/provenance/lifecycle persistence is implemented; physical cleanup is intentionally not automatic.
- Guide sessions remain in-memory until project creation.
- Producer planning is implemented with validated JSON parsing and project-version storage; live execution of a Producer plan is still pending.

## Verification rule

Do not mark this block as fully verified until the GitHub CI run for checkpoint 9226eb0d15a597c9e323cf3bde65af922a417887 is green.
