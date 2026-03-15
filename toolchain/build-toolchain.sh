#!/usr/bin/env bash
set -euo pipefail

PREFIX="${1:-/tools}"

cat <<EON
MaxisOS Toolchain Build (LFS-style)

Target prefix: $PREFIX

Expected steps:
1) Build binutils
2) Build gcc (pass 1)
3) Install Linux headers
4) Build glibc
5) Build gcc (pass 2)

This script is intentionally an outline. See docs/MAXISOS_GUIDE.md for detailed steps.
EON
