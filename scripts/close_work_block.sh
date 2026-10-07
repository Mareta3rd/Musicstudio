#!/usr/bin/env bash
set -euo pipefail
printf "%s\n" "== MUSICSTUDIO WORK BLOCK CLOSE CHECK =="
bash scripts/sync_work_block.sh
printf "\n%s\n" "1) Complete test suite"
python scripts/test.py
printf "\n%s\n" "2) Whitespace check"
git diff --check
printf "\n%s\n" "3) Working tree"
git status --short
printf "\n%s\n" "4) Diff summary"
git diff --stat
printf "\n%s\n" "5) Final sync check"
bash scripts/sync_work_block.sh --check-only
printf "\n%s\n" "6) Checkpoint"
git rev-parse --short HEAD
cat <<EOF

NEXT STEPS
- Confirm no generated artifacts or secrets are present.
- Commit and push the coherent block.
- Update docs/AI_HANDOFF.md.
- Stop at the stable checkpoint.
EOF
