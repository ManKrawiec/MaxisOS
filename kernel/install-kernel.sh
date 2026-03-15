#!/usr/bin/env bash
set -euo pipefail

KERNEL_SRC="${1:-}"
ROOTFS="${2:-}"

if [[ -z "$KERNEL_SRC" || -z "$ROOTFS" ]]; then
  echo "Usage: $0 /path/to/linux /path/to/rootfs"
  exit 1
fi

cd "$KERNEL_SRC"
make INSTALL_MOD_PATH="$ROOTFS" modules_install
make INSTALL_PATH="$ROOTFS/boot" install
