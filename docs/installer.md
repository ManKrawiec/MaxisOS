# Installer (maxinstall)

`maxinstall` is a terminal installer designed for the live ISO.

## Features
- Disk detection via `lsblk`
- Automatic or manual partitioning
- Boot mode selection (UEFI or BIOS)
- Filesystem selection (ext4/btrfs)
- Base system install via `mkpkg`
- Kernel install
- Locale/timezone/keyboard configuration
- User creation
- Hostname and basic network configuration
- GRUB bootloader installation (UEFI or BIOS)

## Usage
Run inside the live environment:
```
maxinstall
```
To apply changes, re-run with:
```
maxinstall --execute
```

## Notes
- Repository paths are configured to `/repo/*` during install.
- For custom layouts, use manual partitioning and mount points.
