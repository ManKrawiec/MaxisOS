#!/usr/bin/env bash
set -euo pipefail

ROOTFS="${1:-}"
if [[ -z "$ROOTFS" ]]; then
  echo "Usage: $0 /path/to/rootfs"
  exit 1
fi

mkdir -p "$ROOTFS"/{bin,boot,dev,etc,home,lib,proc,root,sbin,sys,tmp,usr,var}
mkdir -p "$ROOTFS"/usr/{bin,lib,sbin,share,src}
mkdir -p "$ROOTFS"/var/{log,lib/mkpkg,cache/mkpkg}
mkdir -p "$ROOTFS"/etc/mkpkg
mkdir -p "$ROOTFS"/home/maxis

# Basic config placeholders
cat > "$ROOTFS"/etc/hostname <<'EOC'
maxisos
EOC

cat > "$ROOTFS"/etc/locale.conf <<'EOC'
LANG=en_US.UTF-8
EOC

cat > "$ROOTFS"/etc/timezone <<'EOC'
UTC
EOC

cat > "$ROOTFS"/etc/profile <<'EOC'
export LANG=en_US.UTF-8
export PS1="maxis@maxisos:\\w\\$ "
EOC

cat > "$ROOTFS"/etc/mkpkg/repos.conf <<'EOC'
# One repo path per line
/repo/core
/repo/extra
/repo/community
EOC

cat > "$ROOTFS"/etc/passwd <<'EOC'
root:x:0:0:root:/root:/bin/bash
maxis:x:1000:1000:MaxisOS User:/home/maxis:/bin/bash
EOC

cat > "$ROOTFS"/etc/group <<'EOC'
root:x:0:
wheel:x:10:maxis
users:x:1000:maxis
EOC

cat > "$ROOTFS"/etc/shadow <<'EOC'
root:!:19000:0:99999:7:::
maxis:!:19000:0:99999:7:::
EOC

cat > "$ROOTFS"/etc/sudoers <<'EOC'
root ALL=(ALL) ALL
%wheel ALL=(ALL) ALL
EOC

cat > "$ROOTFS"/etc/fstab <<'EOC'
# <fs> <mountpoint> <type> <opts> <dump> <pass>
EOC

chmod 700 "$ROOTFS"/root
chmod 1777 "$ROOTFS"/tmp

echo "Rootfs prepared at $ROOTFS"
