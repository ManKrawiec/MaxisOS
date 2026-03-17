# Recovery

## Fixing Boot Problems
1. Boot the live ISO.
2. Mount the root filesystem:
```
mount /dev/<root-part> /mnt
mount /dev/<boot-part> /mnt/boot
```
3. Reinstall GRUB:
```
grub-install --target=x86_64-efi --efi-directory /mnt/boot --bootloader-id MaxisOS
chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg
```

## Rebuilding the Kernel
```
./kernel/configure-kernel.sh /path/to/linux
./kernel/build-kernel.sh /path/to/linux
./kernel/install-kernel.sh /path/to/linux /mnt
```

## Debugging Package Errors
- Reinstall the package:
```
mkpkg install <pkg>
```
- Rebuild:
```
mkbuild /path/to/PKGBUILD
```

## Rebuilding the ISO
```
cd iso
./build-iso.sh
```
