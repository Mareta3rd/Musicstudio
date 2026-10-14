
# Musicstudio — Runtime topology

## Recommended topology

The recommended zero-cost setup is hybrid.

### Node A — Control / Desktop
Your own computer.

Runs:
- Musicstudio UI
- project database
- file library
- lightweight agents
- audio playback
- MIDI
- deterministic DSP
- local worker when practical

### Node B — Codespace
Temporary development environment.

Runs:
- source code
- tests
- web backend
- CI reproduction
- documentation work

It is not the default home for heavyweight music-model inference.

### Node C — Optional AI Worker
Any machine with enough GPU/CPU resources.

Runs:
- ACE-Step
- separation
- analysis
- future models

It exposes capabilities to the Control node.

### Node D — Optional remote service
Only for explicit opt-in providers.

## Root controller

The controller exposes one API.

Workers announce:

    worker_id
    capabilities
    health
    compute class
    queue size

Tasks specify:

    capability
    input assets
    resource limits
    cost policy
    deadline
    output contract

The scheduler can then choose:

same machine
or
Codespace
or
remote worker
or
optional cloud provider

without changing the UI.

## Why this matters

The project must scale by adding workers, not by rewriting the application.

A weak PC can still operate the Studio.

A stronger machine can become a worker.

A second PC can become another worker.

A future GPU server can be added without changing the project format.

## Interfaces

The same project API should support:

- browser
- desktop shell
- CLI
- future mobile companion

## Security

Workers authenticate to the controller.

Local-only mode should work without any internet dependency after installation.

Remote workers must never receive more project data than the task requires.

Provider API keys belong to the provider adapter configuration, never to the browser.

## Zero-cost operating mode

Default:

    local UI
    local project
    local deterministic processing
    local open models where feasible
    Codespaces only when actively developing

Paid provider:

    disabled

Optional cloud:

    disabled

Unknown asset provenance:

    non-destructive / review-required
