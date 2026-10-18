# Linux System Audit

A lightweight Python automation lab that collects basic system information
from a Linux workstation.

## Objectives

- Practice Python fundamentals and functions.
- Read operating system information.
- Retrieve memory metrics from `/proc/meminfo`.
- Inspect filesystem capacity and available space.
- Use a Python virtual environment.
- Validate code and tests before committing changes to Git.

## Requirements

- Linux
- Python 3.14 or a compatible Python 3 version supporting
  `platform.freedesktop_os_release()`
- No third-party Python packages required

## Setup

From this directory, create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

## Run the audit

    python system_audit.py

The script reports:

- Operating system and distribution
- Linux kernel and machine architecture
- Python version
- Logical CPU count
- Total and available memory
- Total and free space on the root filesystem

Memory information is read from `/proc/meminfo`. Filesystem information
is collected using Python's standard library.

## Validate the script

Check syntax:

    python -m py_compile system_audit.py

Run the automated tests:

    python -m unittest discover -s tests -v

## Project structure

    linux-system-audit/
    ├── .gitignore
    ├── README.md
    ├── system_audit.py
    └── tests/
        └── test_system_audit.py

The `.venv/` directory is generated locally and must not be committed.

## Limitations

- Memory and filesystem values change as the system runs.
- Filesystem measurements refer to `/`, not every mounted filesystem.
- The script currently targets Linux because it reads `/proc/meminfo`.

## Learning outcomes

This project demonstrates basic Linux system inspection, Python scripting,
virtual environment management, syntax validation, and automated testing.
