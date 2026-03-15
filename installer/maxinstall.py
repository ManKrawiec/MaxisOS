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


def main():
    execute = "--execute" in sys.argv

    console.print("MaxisOS Live Environment")
    console.print("Terminal installer: maxinstall\n")

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
        boot_part = f"{plan.disk}1"
        root_part = f"{plan.disk}2"
    else:
        console.print("Manual partitioning selected. Please partition and then enter boot/root partitions.")
        boot_part = Prompt.ask("Boot partition (e.g. /dev/sda1)")
        root_part = Prompt.ask("Root partition (e.g. /dev/sda2)")

    if plan.filesystem == "ext4":
        run(["mkfs.ext4", root_part], execute)
    else:
        run(["mkfs.btrfs", root_part], execute)

    run(["mkfs.fat", "-F", "32", boot_part], execute)
    run(["mount", root_part, plan.mountpoint], execute)
    run(["mkdir", "-p", f"{plan.mountpoint}/boot"], execute)
    run(["mount", boot_part, f"{plan.mountpoint}/boot"], execute)

    # Install base packages via mkpkg (assumes repos are mounted in /repo)
    base_pkgs = [
        "linux", "bash", "coreutils", "grep", "sed", "gawk", "tar", "gzip",
        "xz", "make", "diffutils", "findutils", "shadow", "util-linux",
        "nano", "vim", "sudo", "networkmanager"
    ]
    for p in base_pkgs:
        run(["mkpkg", "install", p], execute)

    if plan.arch_imports == "yes":
        arch_pkgs = ["htop", "tmux", "git", "neovim", "python", "gcc", "nano", "vim"]
        for p in arch_pkgs:
            run(["/tools/import-arch-pkgbuild.sh", p, f"/repo/extra-sources/{p}", "packages", "extra"], execute)
            run(["mkbuild", "--no-install", f"/repo/extra-sources/{p}/PKGBUILD"], execute)
            run(["cp", f"/repo/extra-sources/{p}/out/{p}.mkpkg", "/repo/extra/"], execute)
            run(["mkpkg", "install", p], execute)

    # Kernel install (expects kernel already built)
    run(["/kernel/install-kernel.sh", "/kernel/src", plan.mountpoint], execute)

    # Generate fstab
    run(["genfstab", "-U", plan.mountpoint], execute)

    # Bootloader
    if plan.bootloader == "grub":
        run(["grub-install", "--target=x86_64-efi", "--efi-directory", f"{plan.mountpoint}/boot", "--bootloader-id", "MaxisOS"], execute)
        run(["grub-mkconfig", "-o", f"{plan.mountpoint}/boot/grub/grub.cfg"], execute)

    console.print("\nInstall complete. You can now chroot and finish configuration.")


if __name__ == "__main__":
    main()
