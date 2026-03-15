#!/usr/bin/env bash
set -euo pipefail

KERNEL_SRC="${1:-}"
JOBS="${JOBS:-$(nproc)}"

if [[ -z "$KERNEL_SRC" ]]; then
  echo "Usage: $0 /path/to/linux"
  exit 1
fi

cd "$KERNEL_SRC"
make -j"$JOBS"
make -j"$JOBS" modules
