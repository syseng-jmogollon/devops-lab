# System Audit — VIT M2400

**Audit date:** 2026-10-19

**Purpose:** Document the workstation's current hardware and operating
environment for the DevOps lab.

## 1. Operating system

- Distribution: Ubuntu Server 26.04.1 LTS.
- Installation: Minimal system with XFCE desktop environment.
- Kernel: Linux 7.0.0-38-generic.
- Architecture: x86_64.

## 2. Processor

- Model: Intel Core i3 M 330.
- Base frequency: 2.13 GHz.
- Physical cores: 2.
- Logical processors: 4.
- VT-x: Reported by the processor.
- AVX, AVX2 and AES instruction flags: Not present in the collected
  CPU flags.
- KVM interface verified for the current user; API version 12.
  Actual VM creation and execution not yet tested.

## 3. RAM

### Current configuration

- Installed memory: 6 GB, configured as 4 GB + 2 GB.
- Memory type reported by SMBIOS: DDR3 SO-DIMM.
- Module speed reported by SMBIOS: 1334 MT/s; actual operating speed not independently confirmed.
- Linux MemTotal: 5,330,012 kB (approximately 5.08 GiB).
- Subsequent virtualization preflight snapshot (2026-10-19): 5.1 GiB
  total RAM, 1.9 GiB available, and 408 MiB swap in use. This is a
  transient reading that may change with workload.
- SMBIOS-reported maximum capacity: 16 GB.
- SMBIOS-reported memory device positions: 4.

### Observed limit and evidence

The SMBIOS information is inconsistent with the physical configuration
and the results of the memory tests.

The installed BIOS reports version `1.02.01GB`. GIGABYTE describes
this BIOS release as fixing incorrect memory-size display in 64-bit
Windows. This is relevant background, but does not establish whether
the SMBIOS memory fields reported to Ubuntu are reliable.

The user reports that the laptop recognized no more than 8 GB in both
of these configurations:

- A single 8 GB memory module.
- An 8 GB module combined with a 4 GB module.

The processor specification lists a maximum memory capacity of 8 GB.
GIGABYTE's published E1425M documentation is inconsistent about the
maximum capacity: its specifications page lists 4 GB, while a manual
table indicates 4 GB x 2.

### Working conclusion

- Practical maximum observed: 8 GB.
- Confidence: Supported by the processor specification and user-reported
  hardware tests.
- SMBIOS value of 16 GB: Not treated as reliable.
- Upgrade recommendation: Do not purchase memory until the target
  module's compatibility and configuration have been checked.

The 8 GB conclusion is the practical limit for planning purposes; it
should not be represented as an unambiguous manufacturer specification.

### References

- Intel Core i3-330M specifications:
  https://www.intel.com/content/www/us/en/products/sku/47663/intel-core-i3330m-processor-3m-cache-2-13-ghz/specifications.html
- GIGABYTE E1425M specifications:
  https://www.gigabyte.com/il/Laptop/E1425M/sp
- GIGABYTE E1425M BIOS and support history:
  https://www.gigabyte.com/Laptop/E1425M/support
- GIGABYTE E1425 series manual:
  https://download1.gigabyte.com/Files/Manual/E1425-Manual-EN.PRC-v1.0.pdf?v=c8f260f0631c19fae53c8eda5b1a0d42

## 4. Storage

- Primary SSD: ADATA SU750, approximately 476.9 GiB as reported by
  `lsblk`.
- Partitioning: GPT layout with a 2 GiB ext4 `/boot` partition and an
  LVM physical volume.
- LVM volume group: `ubuntu-vg`.
- Root logical volume: `ubuntu-lv`, 100 GiB.
- Reported unallocated space in the volume group: approximately 374.93 GiB.
- Swap: `/swap.img`, 4 GiB; previous audit reported zero swap in use.
- Secondary HDD: The user confirms that the WDC HDD and optical-bay
  caddy have been physically removed.

### Drive health

`smartmontools` was not installed at the time of the audit, so current
SMART health and temperature have not been verified.

A historical report recorded a passing SMART status for the ADATA SSD,
approximately 8,336 power-on hours and a temperature around 69°C.
These are historical readings, not a current health assessment.

## 5. Virtualization and CPU capabilities

The CPU flags include `vmx`, indicating advertised Intel VT-x support.

The `kvm` and `kvm_intel` kernel modules are loaded. `/dev/kvm` exists,
and the current user successfully opened the device and queried KVM API
version 12. This confirms access to the KVM interface, but does not yet
prove that a virtual machine can be created and run successfully.

QEMU executables, `qemu-img`, `virsh`, `virt-install`, and `virt-manager`
were not available during the subsequent inventory. The checked QEMU,
libvirt, and virtinst packages were not installed. No guest virtual
machine has been launched yet.

## 6. Audit limitations and next checks

- SMBIOS reports four memory positions, but the known physical
  configuration has two slots.
- The current SMART status of the SSD remains unverified.
- KVM device availability and current-user access are verified; actual
  VM creation and execution remain unverified.
- No software was installed as part of the hardware audit.
- These findings describe the system at the time of the audit and
  should be updated if the hardware or software configuration changes.
