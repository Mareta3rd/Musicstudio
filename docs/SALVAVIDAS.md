# 🛟 SALVAVIDAS — MUSICSTUDIO

Last updated: 2026-10-02
Working branch: foundation/studio-core
Current checkpoint: 0975050eba1fa838cd97b4552eb632db25c3aa68

## 1. DE DÓNDE VENIMOS

Musicstudio is a local-first AI music creation studio rather than a thin wrapper around a single web generator.

The Studio owns creative intent, projects, versions, jobs, metadata, provider selection and history. Generation engines remain replaceable capabilities.

## 2. DÓNDE ESTAMOS

Implemented foundation:
- FastAPI Studio shell and responsive UI
- provider abstraction, Mock provider and ACE-Step REST adapter
- project/version/state persistence in SQLite
- asset catalog and specialist task queue
- Creative Guide and Producer planning bridge
- bounded Lyricist/Prosody execution with audit records
- specialist registry and optional free/local assistant providers
- release/album domain
- control-plane abstraction and addon foundation
- Codespaces workflow, CI and closed work-block protocol

Latest engineering block:
- ACE-Step provider made transport-injectable for deterministic HTTP integration tests.
- REST success handling now accepts both numeric and string `200`.
- Added tests covering submission payloads, completed-result metadata normalization, audio download URL handling and provider failures.

Verification state:
- Previous ACE-Step contract block failed one test because query_result "code" could be a string; that defect was corrected.
- Current code checkpoint 0975050eba1fa838cd97b4552eb632db25c3aa68 is CI-verified in Python 3.11 and 3.12.
- Deterministic ACE-Step tests now cover submission, status/result normalization, audio retrieval, failure handling and health preflight.
- No real ACE-Step generation has been executed yet; that still requires the target runtime/hardware.

## 3. HACIA DÓNDE VAMOS


Immediate sequence:
1. Close verification of checkpoint 9226eb0d15a597c9e323cf3bde65af922a417887.
2. Run/verify Guide -> persistent Project -> Producer plan -> task queue.
3. Verify first live Lyricist task through the configured free assistant.
4. Connect a real ACE-Step 1.5 instance and verify one complete generation to browser playback.
5. Only after the real audio path is stable, expand into reference audio, editing/remix, timeline, stems and finished export.

## 4. ⚠️ NO TOCAR / DECISIONES FIJADAS

- The Studio must not be tightly coupled to one generation model.
- Providers remain local, remote or mocked behind the same boundary.
- Every important development block must leave the repository runnable.
- Free/local components come first; paid services never activate silently.
- UI and architecture must adapt from desktop to smaller screens.
- Do not accumulate large amounts of untested code before closing a milestone.
- Zero-cost operation must remain viable.
- API keys are secrets and never belong in source files, commits or chat messages.
- Autonomous refinement is bounded and auditable.
- Canonical project state belongs to Musicstudio, not to an external model/provider.

## 5. RECOVERY PROCEDURE

1. Read this file.
2. Inspect the latest commit on `foundation/studio-core`.
3. Verify the latest CI/checkpoint.
4. Run `bash scripts/start_work_block.sh` in the Codespace.
5. Start in Mock mode before touching a real provider.
6. Check the latest PR/issues and continue from the single primary next target.
7. When an API key is configured, verify only its presence, never its value.
