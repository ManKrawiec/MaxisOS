#!/usr/bin/env bash
set -euo pipefail

PKG="${1:-}"
DEST="${2:-}"
BRANCH="${3:-packages}"
REPO="${4:-extra}"

if [[ -z "$PKG" || -z "$DEST" ]]; then
  echo "Usage: $0 <pkgname> <dest-dir> [branch] [repo]"
  echo "Example: $0 htop packages/htop packages extra"
  exit 1
fi

mkdir -p "$DEST"

BASE_URL="https://gitlab.archlinux.org/archlinux/$BRANCH/$REPO/$PKG/-/raw/master"

fetch() {
  local file="$1"
  local url="$BASE_URL/$file"
  local out="$DEST/$file"
  if command -v curl >/dev/null 2>&1; then
    curl -L -o "$out" "$url"
  elif command -v wget >/dev/null 2>&1; then
    wget -O "$out" "$url"
  else
    echo "curl or wget required"
    exit 1
  fi
}

fetch PKGBUILD
# Optional install script
fetch "$PKG.install" || true

# Normalize for MaxisOS (optional tweaks)
if [[ -f "$DEST/PKGBUILD" ]]; then
  sed -i 's/^pkgrel=.*/pkgrel=1/' "$DEST/PKGBUILD" || true
fi

echo "Imported $PKG into $DEST"
