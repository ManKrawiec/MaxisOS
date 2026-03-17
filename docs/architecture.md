# Architecture

MaxisOS is a Linux From Scratch (LFS) style system with an Arch-like workflow.

## Principles
- Simple and minimal base system
- Rolling release via local package repos
- Terminal-first usage
- PKGBUILD-compatible build recipes

## Repository Layout
- kernel/: kernel build, install, update scripts
- toolchain/: temporary toolchain build steps
- base-system/: rootfs preparation and base build
- packages/: PKGBUILD recipes (source-based)
- repo/: local binary repos (core/extra/community)
- mkpkg/: package manager for .mkpkg
- mkbuild/: PKGBUILD builder
- installer/: terminal installer (maxinstall)
- iso/: live ISO build system
- scripts/: helper utilities (e.g. PKGBUILD import)
- docs/: documentation

## Build Flow (High Level)
1. Build toolchain in a temporary prefix.
2. Build base system into a rootfs directory.
3. Build packages with mkbuild into .mkpkg files.
4. Publish .mkpkg into repo/ for installation with mkpkg.
5. Install base system and kernel with maxinstall or manually.
6. Generate ISO for live install environment.

## Packaging Model
- Source recipes use PKGBUILD format.
- mkbuild builds into a staging dir and produces .mkpkg.
- mkpkg installs .mkpkg into a target root.

## Rolling Release
- Rebuild packages when upstream changes.
- Replace .mkpkg in repo/ and reinstall with mkpkg.
