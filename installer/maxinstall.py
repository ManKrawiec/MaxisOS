#!/usr/bin/env python3
import os
import sys
import subprocess
from dataclasses import dataclass
from typing import List

try:
    from rich.console import Console
    from rich.prompt import Prompt
except ImportError:
    print("rich not installed. Please install rich or run in the live ISO with it available.")
    sys.exit(1)

console = Console()

@dataclass
class InstallPlan:
    language: str
    keyboard: str
    timezone: str
    disk: str
    partitioning: str
    filesystem: str
    mountpoint: str
    bootloader: str
    root_password: str
    username: str
    user_password: str
    desktop: str
    network: str
    arch_imports: str


def run(cmd: List[str], execute: bool):
    if execute:
        console.print(f"[bold]RUN[/bold] {' '.join(cmd)}")
        subprocess.check_call(cmd)
    else:
        console.print(f"[yellow]DRY[/yellow] {' '.join(cmd)}")

def show_disks():
    console.print("\n[bold]Available disks[/bold]")
    try:
        out = subprocess.check_output(["lsblk", "-d", "-o", "NAME,SIZE,MODEL"], text=True)
        console.print(out.strip())
    except Exception as exc:
        console.print(f"[yellow]WARN[/yellow] Unable to list disks: {exc}")

    try:
        out = subprocess.check_output(["lsblk", "-f"], text=True)
        console.print(out.strip())
    except Exception as exc:
        console.print(f"[yellow]WARN[/yellow] Unable to list filesystems: {exc}")

def part_path(disk: str, number: int) -> str:
    if disk[-1].isdigit():
        return f"{disk}p{number}"
    return f"{disk}{number}"


def main():
    execute = "--execute" in sys.argv

    console.print("MaxisOS Live Environment")
    console.print("Terminal installer: maxinstall\n")

    show_disks()

    language = Prompt.ask("Language", default="en_US.UTF-8")
    keyboard = Prompt.ask("Keyboard layout", default="us")
    timezone = Prompt.ask("Timezone", default="UTC")
    disk = Prompt.ask("Disk (e.g. /dev/sda)")
    partitioning = Prompt.ask("Partitioning", choices=["automatic", "manual"], default="automatic")
    filesystem = Prompt.ask("Filesystem", choices=["ext4", "btrfs"], default="ext4")
    mountpoint = Prompt.ask("Mount point", default="/mnt")
    bootloader = Prompt.ask("Bootloader", choices=["grub"], default="grub")
    root_password = Prompt.ask("Root password", password=True)
    username = Prompt.ask("User name", default="maxis")
    user_password = Prompt.ask("User password", password=True)
    desktop = Prompt.ask("Desktop", choices=["none", "xfce", "kde"], default="none")
    network = Prompt.ask("Network", choices=["dhcp", "manual"], default="dhcp")
    arch_imports = Prompt.ask("Import Arch PKGBUILDs", choices=["yes", "no"], default="yes")

    plan = InstallPlan(
        language=language,
        keyboard=keyboard,
        timezone=timezone,
        disk=disk,
        partitioning=partitioning,
        filesystem=filesystem,
        mountpoint=mountpoint,
        bootloader=bootloader,
        root_password=root_password,
        username=username,
        user_password=user_password,
        desktop=desktop,
        network=network,
        arch_imports=arch_imports,
    )

    console.print("\n[bold]Install plan[/bold]")
    console.print(plan)
    console.print("\nExecuting" if execute else "\nDry-run mode. Re-run with --execute to apply.")

    if plan.partitioning == "automatic":
        run(["sgdisk", "--zap-all", plan.disk], execute)
        run(["sgdisk", "-n", "1:0:+512M", "-t", "1:ef00", plan.disk], execute)
        run(["sgdisk", "-n", "2:0:0", "-t", "2:8300", plan.disk], execute)
        boot_part = part_path(plan.disk, 1)
        root_part = part_path(plan.disk, 2)
    else:
        console.print("Manual partitioning selected. Please partition and then enter boot/root partitions.")
        boot_part = Prompt.ask("Boot partition (e.g. /dev/sda1)")
        root_part = Prompt.ask("Root partition (e.g. /dev/sda2)")

    if plan.filesystem == "ext4":
        run(["mkfs.ext4", root_part], execute)
    else:
        run(["mkfs.btrfs", root_part], execute)

    run(["mkfs.fat", "-F", "32", boot_part], execute)
    run(["mkdir", "-p", plan.mountpoint], execute)
    run(["mount", root_part, plan.mountpoint], execute)
    run(["mkdir", "-p", f"{plan.mountpoint}/boot"], execute)
    run(["mount", boot_part, f"{plan.mountpoint}/boot"], execute)

    # Prepare mkpkg repo config inside target root
    run(["mkdir", "-p", f"{plan.mountpoint}/etc/mkpkg"], execute)
    run(["mkdir", "-p", f"{plan.mountpoint}/repo/core", f"{plan.mountpoint}/repo/extra", f"{plan.mountpoint}/repo/community"], execute)
    run(["/bin/sh", "-c", f"printf '%s\\n' /repo/core /repo/extra /repo/community > {plan.mountpoint}/etc/mkpkg/repos.conf"], execute)

    # Install base packages via mkpkg (assumes repos are mounted in /repo)
    base_pkgs = [
        "linux", "bash", "coreutils", "grep", "sed", "gawk", "tar", "gzip",
        "xz", "make", "diffutils", "findutils", "shadow", "util-linux",
        "nano", "vim", "sudo", "networkmanager"
    ]
    for p in base_pkgs:
        run(["mkpkg", "--root", plan.mountpoint, "install", p], execute)

    if plan.arch_imports == "yes":
        arch_pkgs = ["htop", "tmux", "git", "neovim", "python", "gcc", "nano", "vim"]
        for p in arch_pkgs:
            run(["/scripts/import-arch-pkgbuild.sh", p, f"/repo/extra-sources/{p}", "packages", "extra"], execute)
            run(["mkbuild", "--no-install", f"/repo/extra-sources/{p}/PKGBUILD"], execute)
            run(["cp", f"/repo/extra-sources/{p}/out/{p}.mkpkg", "/repo/extra/"], execute)
            run(["mkpkg", "--root", plan.mountpoint, "install", p], execute)

    # Kernel install (expects kernel already built)
    run(["/kernel/install-kernel.sh", "/kernel/src", plan.mountpoint], execute)

    # Locale, timezone, keyboard
    run(["mkdir", "-p", f"{plan.mountpoint}/etc"], execute)
    run(["/bin/sh", "-c", f"echo '{plan.language} UTF-8' > {plan.mountpoint}/etc/locale.gen"], execute)
    run(["/bin/sh", "-c", f"echo 'LANG={plan.language}' > {plan.mountpoint}/etc/locale.conf"], execute)
    run(["/bin/sh", "-c", f"echo 'KEYMAP={plan.keyboard}' > {plan.mountpoint}/etc/vconsole.conf"], execute)
    run(["/bin/sh", "-c", f"echo '{plan.timezone}' > {plan.mountpoint}/etc/timezone"], execute)
    run(["chroot", plan.mountpoint, "ln", "-sf", f"/usr/share/zoneinfo/{plan.timezone}", "/etc/localtime"], execute)
    run(["chroot", plan.mountpoint, "locale-gen"], execute)

    # Users
    run(["chroot", plan.mountpoint, "/bin/sh", "-c", f"echo 'root:{plan.root_password}' | chpasswd"], execute)
    run(["chroot", plan.mountpoint, "useradd", "-m", "-G", "wheel", "-s", "/bin/bash", plan.username], execute)
    run(["chroot", plan.mountpoint, "/bin/sh", "-c", f"echo '{plan.username}:{plan.user_password}' | chpasswd"], execute)

    # Generate fstab
    run(["/bin/sh", "-c", f"genfstab -U {plan.mountpoint} > {plan.mountpoint}/etc/fstab"], execute)

    # Bootloader
    if plan.bootloader == "grub":
        run(["grub-install", "--target=x86_64-efi", "--efi-directory", f"{plan.mountpoint}/boot", "--bootloader-id", "MaxisOS"], execute)
        run(["grub-mkconfig", "-o", f"{plan.mountpoint}/boot/grub/grub.cfg"], execute)

    console.print("\nInstall complete. You can now chroot and finish configuration.")


if __name__ == "__main__":
    main()
