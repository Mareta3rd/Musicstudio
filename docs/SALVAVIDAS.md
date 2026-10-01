
# 🛟 SALVAVIDAS — MUSICSTUDIO

Last updated: 2026-10-02
Working branch: foundation/studio-core

## 1. DE DÓNDE VENIMOS

Musicstudio started as a local experiment to build an AI music generator / music studio rather than merely use an existing web service.

The original development happened locally, so the GitHub repository began almost empty. We are intentionally rebuilding from the repository root instead of trying to reconstruct missing local history.

The key project idea is broader than text-to-song:

Build our own beautiful creative Studio and let the AI engine remain replaceable.

Current research shows a useful split in the ecosystem:

- Suno is moving toward a complete generative production environment with chat-driven creation/editing and traditional DAW-like capabilities.
- Udio exposes upload, extension, inpainting, remix, style transfer and waveform-oriented session workflows.
- ACE-Step 1.5 provides a broad local engine/API surface including generation, reference audio, repainting, cover generation, stems, multi-track generation and metadata control.
- MusicGen remains a useful simple baseline for text-to-music experimentation.

These references influence architecture and UX, not branding or implementation.

## 2. DÓNDE ESTAMOS

GitHub repository: Mareta3rd/Musicstudio
Default branch: main
Working branch: foundation/studio-core

Implemented in this foundation block:

- FastAPI application shell
- clean web studio UI
- provider interface
- Mock provider
- ACE-Step REST provider
- job orchestration
- generation request model
- health and provider endpoints
- audio proxy path for generated results
- automated tests
- architecture documentation
- Codespaces dev container
- Doctor / Test / Run helper scripts
- specialist-agent registry and /api/agents endpoint (expanded to production, lyric, vocal, MIDI, mix, finish, release and album-level roles)
- release/album domain model for singles, mini-releases, EPs, LPs, live and unplugged works
- optional addon manifest/registry foundation
- zero-cost and hybrid runtime strategy

Current limitations:

- Mock mode completes jobs without real audio.
- ACE-Step integration requires an independently running ACE-Step API server for real audio.
- Projects and history are currently in-memory; persistence is the next block.
The specialist agents are currently declared as capabilities, not autonomous model-driven workers. Their execution layer is intentionally postponed until the real audio pipeline is stable.

## 3. HACIA DÓNDE VAMOS

Immediate objective:

Make one real song travel through the whole pipeline:

creative brief -> Musicstudio -> provider -> generation job -> completed result -> browser playback

Then:

project -> versions -> reference audio -> edits/remix -> timeline -> stems/layers -> finished export

The Studio should gradually become more than a generator: a compact local-first creative workstation.

Strategic direction:
- root control plane
- specialist agents with explicit scopes
- local workers by default
- optional remote workers
- optional paid APIs only behind explicit configuration
- project state as the shared source of truth

## 4. ⚠️ NO TOCAR / DECISIONES FIJADAS

- The Studio must not be tightly coupled to one generation model.
- A provider may be local, remote or mocked; the rest of the application should not care.
- Every important development block must leave the repository runnable.
- The SALVAVIDAS is part of the project, not an external note.
- Free/local components come first; external services are added only where they provide a clear capability.
- UI and architecture should work on desktop and adapt to smaller screens.
- Do not accumulate large amounts of untested code before closing a milestone.
- The zero-cost path must remain viable even when optional cloud connectors exist.

## 5. RECOVERY PROCEDURE

When returning after a gap:

1. Read this file.
2. Inspect the latest commit on the working branch.
3. Run the test suite.
4. Start the application in Mock mode.
5. Only then resume the next engineering block.
6. Check the latest issue/PR and continue from the next stated milestone.
