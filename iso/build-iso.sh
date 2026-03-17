#!/usr/bin/env bash
set -euo pipefail

ISO_NAME="maxisos-live.iso"
ISO_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKDIR="${WORKDIR:-$ISO_DIR/iso-build}"
ROOTFS="$WORKDIR/rootfs"

mkdir -p "$ROOTFS" "$WORKDIR/boot/grub"

# Prepare rootfs
"$ISO_DIR/../base-system/prepare-rootfs.sh" "$ROOTFS"

# Install tools into rootfs (placeholder copy)
mkdir -p "$ROOTFS/usr/bin" "$ROOTFS/bin" "$ROOTFS/scripts" "$ROOTFS/repo/extra" "$ROOTFS/repo/extra-sources"
install -m 0755 "$ISO_DIR/../mkpkg/mkpkg" "$ROOTFS/usr/bin/mkpkg"
install -m 0755 "$ISO_DIR/../mkbuild/mkbuild" "$ROOTFS/usr/bin/mkbuild"
install -m 0755 "$ISO_DIR/../installer/maxinstall.py" "$ROOTFS/usr/bin/maxinstall"
install -m 0755 "$ISO_DIR/../scripts/import-arch-pkgbuild.sh" "$ROOTFS/scripts/import-arch-pkgbuild.sh"

# Provide bash if available on host
if [[ -x /bin/bash ]]; then
  install -m 0755 /bin/bash "$ROOTFS/bin/bash"
  ln -sf /bin/bash "$ROOTFS/bin/sh"
fi

# Live environment message
cat > "$ROOTFS/etc/issue" <<'EOM'
MaxisOS Live Environment
EOM

# Minimal init (placeholder)
cat > "$ROOTFS/init" <<'EOM'
#!/bin/sh
echo "MaxisOS Live Environment"
export PATH=/bin:/usr/bin:/scripts
exec /bin/sh
EOM
chmod +x "$ROOTFS/init"

# Merge optional rootfs overrides
if [[ -d "$ISO_DIR/rootfs" ]]; then
  cp -a "$ISO_DIR/rootfs/." "$ROOTFS/"
fi

# Build initramfs (placeholder)
( cd "$ROOTFS" && find . | cpio -H newc -o ) > "$WORKDIR/initrd.img"

# Copy kernel (expects built kernel at ../kernel/bzImage)
cp "$ISO_DIR/../kernel/bzImage" "$WORKDIR/vmlinuz"

# GRUB config
if [[ -f "$ISO_DIR/grub/grub.cfg" ]]; then
  cp "$ISO_DIR/grub/grub.cfg" "$WORKDIR/boot/grub/grub.cfg"
else
  cat > "$WORKDIR/boot/grub/grub.cfg" <<'EOM'
set timeout=5
set default=0

menuentry "MaxisOS Live Environment" {
  linux /vmlinuz
  initrd /initrd.img
}
EOM
fi

# Build ISO
xorriso -as mkisofs -o "$ISO_NAME" \
  -b boot/grub/i386-pc/eltorito.img \
  -no-emul-boot -boot-load-size 4 -boot-info-table \
  -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot \
  "$WORKDIR"

echo "ISO created: $ISO_NAME"
