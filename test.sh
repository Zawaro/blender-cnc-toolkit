#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load .env if present
if [ -f "$SCRIPT_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/.env"
  set +a
fi

run_variant() {
  local addon="$1"
  local blender="$2"

  if [ ! -x "$blender" ]; then
    echo "SKIP  $addon — $blender not found"
    return 0
  fi

  local staging
  staging=$(mktemp -d)
  cp -r "$SCRIPT_DIR/$addon" "$staging/"

  echo "---- $addon ----"
  BLENDER_ADDON="$addon" BLENDER_EXECUTABLE="$blender" \
    uv run pytest --blender-addons-dirs "$staging" -v -- -noaudio
  local rc=$?
  rm -rf "$staging"
  return $rc
}

# Single variant mode: ./test.sh
if [ "${1:-}" != "--all" ]; then
  addon="${BLENDER_ADDON:-hi_five}"
  blender="${BLENDER_EXECUTABLE:-}"
  if [ -z "$blender" ]; then
    echo "Usage: BLENDER_EXECUTABLE=/path/to/blender ./test.sh"
    echo "       ./test.sh --all  (requires BLENDER_5/4/3 in .env)"
    exit 1
  fi
  run_variant "$addon" "$blender"
  exit $?
fi

# All-variant mode: ./test.sh --all
fail=0
[ -n "${BLENDER_5:-}" ] && run_variant hi_five  "$BLENDER_5"  || fail=1
[ -n "${BLENDER_4:-}" ] && run_variant eevee_next "$BLENDER_4" || fail=1
[ -n "${BLENDER_3:-}" ] && run_variant cyclesx  "$BLENDER_3"  || fail=1

if [ "$fail" -ne 0 ]; then
  echo "Some variants failed or were skipped"
  exit 1
fi

echo "All variants passed"
