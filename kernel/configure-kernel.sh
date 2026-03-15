#!/usr/bin/env bash
set -euo pipefail

KERNEL_SRC="${1:-}"
if [[ -z "$KERNEL_SRC" ]]; then
  echo "Usage: $0 /path/to/linux"
  exit 1
fi

cd "$KERNEL_SRC"
make menuconfig
