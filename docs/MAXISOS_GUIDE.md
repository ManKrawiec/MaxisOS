# MaxisOS Guide

This guide describes the structure, build workflow, and usage of MaxisOS.

## 1. System Structure

MaxisOS follows a classic Unix hierarchy:

/
|-- bin
|-- boot
|-- dev
|-- etc
|-- home
|-- lib
|-- proc
|-- root
|-- sbin
|-- sys
|-- tmp
|-- usr
|-- var

Default user: `maxis`
Default shell prompt: `maxis@maxisos:~$`
Default language: English (`en_US.UTF-8`)

Language, keyboard layout, and timezone are chosen during installation.

## 2. Package Manager (mkpkg)

`mkpkg` manages binary packages with the `.mkpkg` extension.

Package layout:
```
package.mkpkg
├── metadata.json
├── files/
└── install.sh (optional)
```

Key paths:
- Package database: `/var/lib/mkpkg`
- Repo configuration: `/etc/mkpkg/repos.conf`

Commands:
- `mkpkg install <pkg|path.mkpkg>`
- `mkpkg remove <pkg>`
- `mkpkg update`
- `mkpkg search <term>`
- `mkpkg list`
- `mkpkg --root /mnt install <pkg>` (install into target root)

## 3. Installing Packages

1. Ensure `/etc/mkpkg/repos.conf` lists your repos.
2. Put `.mkpkg` files into `/repo/core`, `/repo/extra`, or `/repo/community`.
3. Run:
```
mkpkg install <pkgname>
```

## 4. Creating Packages

Use `mkbuild` with a PKGBUILD file (installs by default):

```
mkbuild /path/to/PKGBUILD
```

PKGBUILD basics:
- `pkgname`, `pkgver`, `pkgrel`
- `source=()` and `sha256sums=()`
- `build()` and `package()`

Inside `package()`, install into `$pkgdir`.

## 4.1 Importing Arch PKGBUILDs (Optional)

MaxisOS can import PKGBUILDs from Arch to speed up packaging. This does not use Arch binary packages; it only pulls build scripts.

Example:
```
scripts/import-arch-pkgbuild.sh htop packages/htop packages extra
mkbuild --no-install packages/htop/PKGBUILD
```

This requires network access and `curl` or `wget`.

## 5. Rebuilding the Kernel

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

Updating the kernel source:
```
./kernel/update-kernel.sh <version>
```

## 6. Debugging Kernel Problems

- Use `dmesg` and `journalctl -kb` after boot.
- Boot with `loglevel=7` and `earlyprintk` in the kernel command line.
- Ensure drivers for storage and filesystem are built-in (not only modules).

## 7. Debugging Boot Problems

Checklist:
- Ensure `/boot` contains kernel and initrd.
- Validate `grub.cfg` paths.
- Run `grub-install` again if bootloader missing.
- Use `journalctl -xb` inside chroot for logs.

## 8. Fixing Broken Packages

1. Reinstall the package:
```
mkpkg install <pkgname>
```
2. Remove and reinstall:
```
mkpkg remove <pkgname>
mkpkg install <pkgname>
```
3. If broken deps, rebuild with mkbuild.

## 9. Updating the System

MaxisOS is rolling release. Update by:
1. Rebuilding new packages with `mkbuild`.
2. Copying `.mkpkg` into `/repo/*`.
3. Installing updated packages via `mkpkg install <pkg>`.

## 10. Rebuilding the Init System

MaxisOS uses a simple init within the live ISO. For a full system, decide on:
- `sysvinit`
- `runit`
- `systemd`

Rebuild by packaging the chosen init system via `mkbuild`, install with `mkpkg`, and regenerate initramfs if used.

## 11. Building the ISO

Use the ISO build script:
```
cd iso
./build-iso.sh
```
This script expects a built kernel at `kernel/bzImage` and uses `xorriso`.
On boot, the live environment shows: `MaxisOS Live Environment` and provides the commands `maxinstall`, `mkpkg`, and `bash`.

## 12. QEMU Instructions

Run a built disk image:
```
qemu-system-x86_64 -drive file=maxisos.img,format=raw -m 2048
```

Run the live ISO:
```
qemu-system-x86_64 -cdrom maxisos-live.iso -m 2048
```

## 13. Manual Installation Mode

The live environment also supports manual installation (Arch-like). You can:
- Partition disks manually (`fdisk`, `cfdisk`, `parted`)
- Mount filesystems manually under `/mnt`
- Install packages with `mkpkg install <pkgname>`
- Configure `/etc/locale.conf`, `/etc/timezone`, `/etc/fstab`

## 14. Installer (maxinstall)

Launch in the live environment:
```
maxinstall
```

Steps:
1. Language selection
2. Keyboard layout
3. Timezone
4. Disk selection
5. Partitioning (auto/manual)
6. Filesystem (ext4/btrfs)
7. Mount points
8. Bootloader (GRUB)
9. Root password
10. User creation
11. Optional desktop (none/XFCE/KDE)
12. Network (DHCP/manual)

The installer formats partitions, mounts, installs base packages, installs the kernel, generates fstab, installs bootloader, and configures system defaults.
