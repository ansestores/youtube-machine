#!/usr/bin/env bash
# Ep.11 — run the whole pipeline every day, unattended.
#
# Ep.3-10 built the parts. This is the part that means you stop touching it.
# Tested on macOS (launchd) and Linux (cron).
set -euo pipefail

ROOT="${PIPELINE_ROOT:-$HOME/yshorts}"
LOG="$ROOT/logs/$(date +%Y-%m-%d).log"
mkdir -p "$(dirname "$LOG")"

# Everything below goes to the log AND to stdout, so cron mail is useful too.
exec > >(tee -a "$LOG") 2>&1
echo "=== run $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

# A lock, or two runs overlap and fight over the same files. flock is Linux-only;
# mkdir is atomic everywhere and works on macOS too.
LOCK="$ROOT/.daily.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "another run is still going (lock held) — exiting"; exit 0
fi
trap 'rmdir "$LOCK"' EXIT

cd "$ROOT"
python3 tools/build_slate.py slate/today.json     # render everything for today
python3 uploader/upload_slate.py slate/today.json # upload + schedule + playlists
echo "=== done $(date -u +%H:%M:%SZ) ==="
