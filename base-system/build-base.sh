#!/usr/bin/env bash
set -euo pipefail

ROOTFS="${1:-}"
if [[ -z "$ROOTFS" ]]; then
  echo "Usage: $0 /path/to/rootfs"
  exit 1
fi

# This script is an LFS-style outline. It assumes you already built the toolchain.
# You should run each section in a clean chroot into $ROOTFS.

cat <<'EON'
MaxisOS Base System Build (LFS-style)

1) Build toolchain (binutils, gcc, glibc) into /tools
2) Enter chroot into the rootfs
3) Build and install essential packages in order:
   - linux kernel headers
   - glibc
   - zlib
   - bzip2
   - xz
   - bash
   - coreutils
   - sed
   - grep
   - gawk
   - diffutils
   - findutils
   - make
   - util-linux
   - shadow
   - tar
   - gzip
   - sudo
   - nano
   - vim
   - NetworkManager

This repo provides mkbuild to build packages using PKGBUILD-style scripts.
See docs/MAXISOS_GUIDE.md for detailed steps.
EON
