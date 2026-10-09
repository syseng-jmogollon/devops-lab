# Hardware and Operating Environment

## Purpose

This document records the hardware, operating-system, storage, and troubleshooting findings from the initial assessment of the DevOps Lab machine. It describes the system before the planned clean Fedora installation.

## Hardware Identity

* **System:** VIT M2400 laptop, distributed in Venezuela
* **Underlying platform:** GIGABYTE E1425M
* **BIOS:** Phoenix Technologies LTD 1.02.01GB
* **BIOS date:** October 20, 2011
* **Firmware mode:** Legacy BIOS
* **CPU:** Intel Core i3 M330, 2 cores / 4 threads, 2.13 GHz
* **Memory:** 6 GiB DDR3 (4 GiB + 2 GiB)
* **Operating system at audit time:** Fedora Linux 44 Workstation
* **Kernel at audit time:** 7.2.8-200.fc44.x86_64

The laptop originally had an internal HDD position and an optical DVD drive. The optical drive was replaced with a SATA HDD caddy. The ADATA SSD occupies the original storage position, while the WDC HDD is installed in the caddy.

## Storage Inventory

| Device     | Model                 |     Capacity | Status                    |
| ---------- | --------------------- | -----------: | ------------------------- |
| `/dev/sda` | ADATA SU750           |    476.9 GiB | SMART health PASSED       |
| `/dev/sdb` | WDC WD3200BEKT-60V5T1 |    298.1 GiB | SMART failure; unreliable |
| `/dev/sdc` | Multi-Card            | 0 B reported | Card-reader device        |

### SSD Assessment

* Model: ADATA SU750, 512 GB
* Firmware: XA003R17
* Negotiated SATA link: 3.0 Gb/s; drive supports up to 6.0 Gb/s
* SMART overall health: PASSED
* Reallocated sectors: 0
* UDMA CRC errors: 0
* SMART error log: no errors reported
* Power-on hours: approximately 8,453
* Endurance indicator: 3%
* Reported SMART temperature: approximately 70–71°C

The temperature reading could not be independently verified. With the laptop's bottom cover removed, CPU temperature decreased to approximately 43°C at idle, while the SSD continued to report approximately 70°C.

The available evidence does not establish whether the SSD is physically reaching that temperature or whether the reported value is inaccurate. The available IR thermometer was not verified for reliable measurements at this temperature.

The SSD's reported temperature remains an unresolved monitoring concern. It should not be documented as either a confirmed thermal failure or a confirmed sensor fault.

### HDD Assessment

The WDC HDD reported SMART failure indicators, including:

* 1,219 reallocated sectors
* 526 pending sectors
* 63,575 reported uncorrectable sectors/errors in the collected SMART output

The HDD is unreliable and must not be used for important data or backups.

## Filesystem Audit

The Fedora Btrfs filesystem has label `fedora` and UUID `9d562824-a839-4812-bf94-f7c3a6fe11b1`. It spans two devices.

| Device   | Partition         |       Size | Allocated |
| -------- | ----------------- | ---------: | --------: |
| Device 1 | `/dev/sda3` (SSD) | 474.94 GiB | 46.02 GiB |
| Device 2 | `/dev/sdb1` (HDD) | 298.09 GiB |  1.01 GiB |

At audit time:

* `/` and `/home` were Btrfs subvolumes.
* `/boot` was ext4 on `/dev/sda2`, with a size of 2 GiB.
* Btrfs subvolumes: `root`, `home`, and `var/lib/machines`.
* Data profile: `single`.
* Metadata profile: `RAID1`.
* System profile: `RAID1`.
* Total Btrfs device capacity: approximately 773 GiB.
* Used space: approximately 24 GiB.
* Btrfs device error counters: zero reported errors for both devices at inspection time.

The `single` data profile means file data is not mirrored across the two drives. The metadata and system profiles use RAID1, so the filesystem still relies on the second device for mirrored allocations.

Zero Btrfs error counters do not establish that the failing HDD is healthy. The SMART results remain a significant warning.

## Backup and Recovery Plan

The user confirmed that important data has been backed up to an external hard drive and that the laptop can be formatted.

**Planned action:** perform a clean Fedora installation on the ADATA SU750 SSD alone, with the failed WDC HDD disconnected. Keep the external backup drive disconnected during installation.

Before confirming partitioning or formatting, verify the selected target by its model and capacity.

This is a planned action, not a completed installation. Afterward, update this document with the resulting Fedora version, partition layout, and verification that the failed HDD is no longer part of the active filesystem.

## Lessons Learned

1. A filesystem can span multiple physical devices even when its root filesystem appears to be mounted from one partition.
2. Btrfs data and metadata profiles describe different redundancy properties.
3. Filesystem device-error counters and SMART diagnostics are complementary checks.
4. A verified backup enables a simpler recovery strategy when the existing storage configuration includes a failing device.
5. Technical documentation should distinguish confirmed findings from hypotheses and unresolved measurements.
