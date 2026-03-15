# MaxisOS

MaxisOS is a Linux From Scratch–style distribution blueprint that targets a simple, rolling, terminal‑oriented system inspired by Arch’s philosophy but built from scratch.

This repository provides:
- Base system build scripts (LFS style)
- Kernel build/configure/install scripts
- `mkpkg` package manager
- `mkbuild` PKGBUILD‑style build tool
- Example packages and local repos
- Live ISO build script
- `maxinstall` terminal installer
- Full system documentation

## Quick Start (Dev)
```
./base-system/prepare-rootfs.sh /tmp/maxisos-root
./kernel/configure-kernel.sh /path/to/linux
./kernel/build-kernel.sh /path/to/linux
./kernel/install-kernel.sh /path/to/linux /tmp/maxisos-root
```

See `docs/MAXISOS_GUIDE.md` for the full build, install, and QEMU instructions.
