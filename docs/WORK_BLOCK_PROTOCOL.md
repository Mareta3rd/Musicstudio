# Musicstudio Work Block Protocol

Musicstudio is developed in closed, auditable blocks.

## Shared-branch synchronization

Before starting or resuming:

    git status --short
    bash scripts/sync_work_block.sh

The synchronizer distinguishes GREEN, BEHIND, AHEAD, DIVERGED and BEHIND + DIRTY.

Only a clean branch that is strictly behind may be fast-forwarded automatically.
Local uncommitted work is never overwritten automatically.

## Standard cycle

1. Solve one coherent objective.
2. Verify focused checks and then the complete suite.
3. Inspect status, diff check and diff summary.
4. Save the coherent block with a commit and push.
5. Record branch, checkpoint, tests, decisions and unresolved items in docs/AI_HANDOFF.md.
6. Mark exactly one primary next target.
7. Stop at the stable checkpoint.

## Remote writes

Any remote execution path must refresh the active branch before editing.
After remote writes, the Codespace synchronizes before continuing.

## Closure invariant

solved + synchronized + verified + inspected + committed + pushed + handed-off + next-direction-marked

## Why

The conversation is transient state. The repository is durable state.
