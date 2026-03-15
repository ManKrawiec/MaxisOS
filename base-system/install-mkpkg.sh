#!/usr/bin/env bash
set -euo pipefail

ROOTFS="${1:-}"
if [[ -z "$ROOTFS" ]]; then
  echo "Usage: $0 /path/to/rootfs"
  exit 1
fi

install -d "$ROOTFS/usr/bin"
install -m 0755 "$(dirname "$0")/../mkpkg/mkpkg" "$ROOTFS/usr/bin/mkpkg"
install -m 0755 "$(dirname "$0")/../mkbuild/mkbuild" "$ROOTFS/usr/bin/mkbuild"
