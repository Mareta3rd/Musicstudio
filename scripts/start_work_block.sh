#!/usr/bin/env bash
set -euo pipefail

printf "%s\n" "== MUSICSTUDIO WORK BLOCK START =="
printf "%s\n" "1) Synchronize"
bash scripts/sync_work_block.sh

printf "\n%s\n" "2) Install editable development dependencies"
python -m pip install -e ".[dev]"

printf "\n%s\n" "3) Doctor"
python scripts/doctor.py

printf "\n%s\n" "4) Tests"
python scripts/test.py

printf "\n%s\n" "== READY =="
printf "%s\n" "Branch: $(git branch --show-current)"
printf "%s\n" "Checkpoint: $(git rev-parse --short HEAD)"
