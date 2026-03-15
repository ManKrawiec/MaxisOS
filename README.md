# MaxisOS

MaxisOS is a Linux From Scratch–style distribution project that aims for a simple, rolling, terminal‑oriented system inspired by Arch’s philosophy, but built from source.

## Status: Work in Progress
This repository is under active development. Expect incomplete features, breaking changes, and placeholder tooling while the base system is being built out.

## What This Repo Contains
- LFS‑style base system scaffolding
- Kernel configure/build/install scripts
- `mkpkg` package manager and `.mkpkg` format
- `mkbuild` PKGBUILD‑style builder
- Example PKGBUILDs and local repo layout
- `maxinstall` terminal installer (prototype)
- Live ISO build script (prototype)
- Full documentation and progress tracking

## Quick Start (Dev)
```
./base-system/prepare-rootfs.sh /tmp/maxisos-root
./kernel/configure-kernel.sh /path/to/linux
./kernel/build-kernel.sh /path/to/linux
./kernel/install-kernel.sh /path/to/linux /tmp/maxisos-root
```

## Documentation
- Main guide: `docs/MAXISOS_GUIDE.md`
- Progress: `docs/PROGRESS.md`

## License
MIT License. See `LICENSE`.
