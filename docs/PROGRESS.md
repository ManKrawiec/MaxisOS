# MaxisOS Progress

Last update: 2026-03-15

## Current Stage
LFS-style scaffolding complete.

## Completed
- Project structure created (kernel, toolchain, base-system, packages, repo, mkpkg, mkbuild, installer, iso, docs)
- Base rootfs preparation scripts
- Kernel configure/build/install scripts
- mkpkg package manager
- mkbuild PKGBUILD-style builder
- Example PKGBUILDs and local repo layout
- Live ISO build script (placeholder flow)
- maxinstall terminal installer (optional Arch PKGBUILD import)
- Documentation (MAXISOS_GUIDE.md)
- License and .gitignore

## In Progress
- Real ISO boot pipeline (initramfs, bootloader images)
- Real package build and dependency resolution
- Full installer execution flow (partitioning, chroot, fstab, locale, users)

## Next Steps
- Implement selectable package list in maxinstall
- Add dependency solver for mkpkg
- Add real init system packaging (runit/systemd)
- Build and test ISO in QEMU
