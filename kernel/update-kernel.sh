#!/usr/bin/env bash
set -euo pipefail

# Simple helper to pull a new kernel tarball into kernel/sources.
# You can replace this with git-based workflow if desired.

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <kernel-version>"
  exit 1
fi

mkdir -p "$(dirname "$0")/sources"
cd "$(dirname "$0")/sources"

URL="https://cdn.kernel.org/pub/linux/kernel/v${VERSION%%.*}.x/linux-${VERSION}.tar.xz"

echo "Download: $URL"
if command -v curl >/dev/null 2>&1; then
  curl -LO "$URL"
elif command -v wget >/dev/null 2>&1; then
  wget "$URL"
else
  echo "curl or wget required"
  exit 1
fi
