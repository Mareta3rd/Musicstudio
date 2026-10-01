
# Musicstudio

Musicstudio is an experimental AI music creation studio built as a provider-independent local application.

The project is deliberately split into two layers:

- Musicstudio Studio: the interface, orchestration, job model and creative workflow we own.
- Generation Providers: pluggable engines such as ACE-Step, future local models, or external APIs.

The first milestone is usable without an AI model. The built-in Mock provider exercises the complete application workflow so we can develop the Studio without waiting on model installation.

## Current state

- FastAPI backend
- Single-page studio interface
- Provider abstraction
- Mock provider for zero-dependency generation tests
- ACE-Step REST adapter
- Project direction recorded in docs/SALVAVIDAS.md
- Automated unit tests
- No API key required for the local Studio itself

## Quick start

Python 3.11+ is recommended.

Windows:
    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -U pip
    pip install -e .
    python -m uvicorn musicstudio.app:app --reload

Then open http://127.0.0.1:8000.

The default provider is mock, so the application starts without an AI model.

## Codespaces

The repository includes a `.devcontainer/devcontainer.json` so a new Codespace gets Python 3.12 and project dependencies automatically. Helper commands:

    python scripts/doctor.py
    python scripts/test.py
    python scripts/run.py

The included personal-account Codespaces allowance is finite, so stop the Codespace when finished.

## Production vision

Musicstudio is intended to cover the production chain from brief and lyrics through composition, arrangement, editing, mixing, polish, mastering and delivery. A specialist-agent registry is already part of the foundation; agents will be activated progressively as the underlying audio pipeline becomes reliable.

## Provider modes

Mock:
    MUSICSTUDIO_PROVIDER=mock

ACE-Step:
Run ACE-Step 1.5 separately in REST API mode and point Musicstudio at it:
    MUSICSTUDIO_PROVIDER=ace-step
    ACE_STEP_URL=http://127.0.0.1:8001

ACE-Step documents the local REST flow as release_task -> query_result -> audio retrieval.

## Design principle

Musicstudio should not become a thin wrapper around one model.

The Studio owns:
- projects
- prompts and creative intent
- versions
- generations
- metadata
- provider selection
- history
- future editing and arrangement workflows

Providers own:
- inference
- model-specific parameters
- model limitations
- model-specific audio operations

That separation lets the Studio evolve independently from the model.

## Repository map

docs/
  ARCHITECTURE.md
  SALVAVIDAS.md

src/musicstudio/
  app.py
  config.py
  models.py
  orchestrator.py
  providers/
    base.py
    mock.py
    ace_step.py

tests/
  test_orchestrator.py

web/
  index.html
  styles.css
  app.js

## Roadmap

1. Real ACE-Step generation and audio playback
2. Project persistence
3. Generation history and versioning
4. Audio upload plus reference/cover/remix flows
5. Timeline and arrangement workspace
6. Stems and layer workflow
7. Creative assistant for prompt and song structure
8. Additional local and cloud providers

Every block should remain independently runnable and documented by the SALVAVIDAS.
