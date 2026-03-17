# Kernel

## Scripts
- configure: `kernel/configure-kernel.sh <path-to-linux-src>`
- build: `kernel/build-kernel.sh <path-to-linux-src>`
- install: `kernel/install-kernel.sh <path-to-linux-src> <rootfs>`
- update: `kernel/update-kernel.sh <version>`

## Rebuilding the Kernel
1. Configure:
```
./kernel/configure-kernel.sh /path/to/linux
```
2. Build:
```
./kernel/build-kernel.sh /path/to/linux
```
3. Install into rootfs:
```
./kernel/install-kernel.sh /path/to/linux /mnt
```

## Initramfs
The live ISO builds a simple initramfs from the rootfs staging directory.
For installed systems, choose your initramfs strategy (e.g. dracut, mkinitcpio,
or a custom init) and package it via `mkbuild`.

## Troubleshooting
- Check `dmesg` and `journalctl -kb` after boot.
- Ensure storage and filesystem drivers are built-in or included in initramfs.
- Add `loglevel=7` to the kernel command line for verbose output.
