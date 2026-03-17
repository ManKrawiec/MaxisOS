# Arch Compatibility Layer

This directory provides a minimal Arch Linux package installer for MaxisOS.

## Components
- `pacman`: compatibility installer (supports `pacman -S <pkg>`)
- `mirrorlist.example`: sample mirror configuration

## Installation Paths
- Installer: `/usr/lib/maxisos/arch-compat/pacman`
- Wrapper: `/usr/bin/pacman`
- Mirrorlist: `/etc/pacman.d/mirrorlist`
- Database: `/var/lib/pacman/`

## Notes
- This is a compatibility layer, separate from `mkpkg`.
- It downloads Arch packages, checks dependencies, and installs files.
- Compatibility warnings are shown when glibc/library or path mismatches are detected.
