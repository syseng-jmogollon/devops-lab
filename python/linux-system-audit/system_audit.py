#!/usr/bin/env python3

"""Collect a basic system audit on a Linux workstation."""

import os
import platform
import shutil
from pathlib import Path


def get_memory_info():
    """Return total and available memory from /proc/meminfo."""
    memory = {}

    with Path("/proc/meminfo").open(encoding="utf-8") as file:
        for line in file:
            key, value = line.split(":", maxsplit=1)
            if key in {"MemTotal", "MemAvailable"}:
                memory[key] = int(value.strip().split()[0])

    return memory


def main():
    print("=== Linux System Audit ===")
    print(f"Operating system: {platform.system()}")
    print(f"Distribution: {platform.freedesktop_os_release()['PRETTY_NAME']}")
    print(f"Kernel: {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print(f"Logical CPUs: {os.cpu_count()}")

    memory = get_memory_info()
    print(f"Total memory: {memory['MemTotal'] / 1024:.0f} MiB")
    print(f"Available memory: {memory['MemAvailable'] / 1024:.0f} MiB")

    disk = shutil.disk_usage("/")
    print(f"Root filesystem total: {disk.total / (1024**3):.1f} GiB")
    print(f"Root filesystem free: {disk.free / (1024**3):.1f} GiB")


if __name__ == "__main__":
    main()
