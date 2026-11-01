# System Audit — VIT M2400

**Audit date:** 2026-10-19
**Last updated:** 2026-10-28 (RAM detection troubleshooting, Docker installation, libvirt access model)

**Purpose:** Document the workstation's current hardware and operating
environment for the DevOps lab.

## 1. Operating system

- Distribution: Ubuntu 26.04.1 LTS.
- Installation: Minimal system with XFCE desktop environment; the
  `ubuntu-desktop` metapackage is not installed.
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
- KVM interface verified; API version 12.
- A TinyCore guest was created and launched successfully during a
  subsequent virtualization test. It received a DHCP address from the
  libvirt default NAT network.
- The test guest was removed after the test; no guest VM is currently
  registered with libvirt (`sudo virsh list --all`, 2026-10-26).

## 3. RAM

### Current configuration

- Installed memory: 6 GB, configured as 4 GB + 2 GB.
- Memory type reported by SMBIOS: DDR3 SO-DIMM.
- Module speed reported by SMBIOS: 1334 MT/s; actual operating speed not independently confirmed.
- Linux MemTotal (baseline measurement, 2026-10-19): 5,330,012 kB
  (approximately 5.08 GiB).
- Subsequent virtualization preflight snapshot (2026-10-19): 5.1 GiB
  total RAM, 1.9 GiB available, and 408 MiB swap in use. This is a
  transient reading that may change with workload.
- Linux `free -h` after the correction (2026-10-26): 5.1 GiB total.
- SMBIOS-reported maximum capacity: 16 GB.
- SMBIOS-reported memory device entries: 4 (see the limitations section).

### Detection fault and correction (2026-10-22 to 2026-10-26)

**Status:** Resolved (verified after physical correction).

**Symptom.** On 2026-10-22 at approximately 20:24 (local time), `free -h`
reported approximately 3.3 GiB of total memory, below the baseline above.
The figure was reported by the operator; the original output was not
archived.

**Investigation.** Two read-only checks were used:

    free -h
    sudo dmidecode -t memory | grep -E 'Size|Locator|Speed|Configured'

Before the correction, the firmware reported two installed modules
(4 GB and 2 GB, 1334 MT/s) and two empty slots. These observations were
reported by the operator and are not archived as raw output.

**Root cause.** Physical inspection found that the 2 GB module was not
properly seated after hardware maintenance. The module was reseated.
This explanation is supported by the before-and-after change below.

**Verification.** On 2026-10-26, after the correction and power-on:

- `free -h` reported 5.1 GiB of total memory.
- `dmidecode` reported `M1` with a 4 GB module and `M2` with a 2 GB
  module, both at 1334 MT/s; `M3` and `M4` reported no module installed.
- Docker reported 5.083 GiB of total memory after its daemon started on
  the same day, consistent with the `free` reading.

The nominal capacity is 6 GB (about 5.6 GiB). The difference between
nominal capacity and the value reported by Linux was not measured; it is
consistent with memory reserved by the platform, but that has not been
verified.

**Conclusion.** The memory-detection issue was resolved by reseating the
improperly seated module. Both installed modules are detected. No
operating-system reinstallation or software configuration change was
required.

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
- Defective HDD: The WDC HDD was physically removed.
- Optical-bay caddy: It was initially removed along with the defective
  HDD. It was subsequently reused to house the ADATA SU750 SSD after
  lower SSD temperatures were observed in that configuration.
- Current SSD placement: The ADATA SU750 remains installed in the
  optical-bay caddy.
- The built-in USB Multi-Card reader is detected as a zero-capacity
  device (`/dev/sdb` in the latest observation). Device names may change
  across boots or hardware changes.

### Drive health and thermal observations

`smartmontools` version `7.5-2` was installed by the operator with
`sudo apt install smartmontools -y` at 19:53:47 on 2026-10-20 (local
time), as recorded in the `sudo` journal and the `dpkg` log (installation
between 19:53:53 and 19:53:56). The first SMART query that day was
`sudo smartctl -H -A` on the SSD at 19:54:37.

The latest observed SSD was `/dev/sda`, identified by model as
ADATA SU750, with approximately 476.9 GiB reported by `lsblk`.

A 10-minute idle observation on 2026-10-21 recorded temperatures
of 64°C at the start and 63°C at the end.

The subsequent SMART check, performed at approximately 21:48 on
2026-10-21 (Caracas time, UTC-04:00), reported:
- Overall SMART self-assessment: `PASSED`.
- Power-on hours: 8,592.
- Reallocated sector count (ID 5): 0.
- Reallocated event count (ID 196): 0.
- UDMA CRC error count (ID 199): 0.
- Temperature (ID 194): 63°C.

Earlier observations recorded temperatures around 69–71°C with the SSD
in the primary SATA bay. After moving the SSD to the optical-bay caddy,
observed readings were approximately 63–66°C. This reduction motivated
the decision to reuse the caddy for the SSD. The comparison is
observational, not a controlled thermal test, and does not establish
that the caddy alone caused the temperature reduction.

During the latest 10-minute observation, the block-device counters
recorded 1,624 sectors read and 10,728 sectors written. Assuming 512-byte
sectors, this corresponds to approximately 812 KiB read and 5.24 MiB
written. These counters do not identify which process generated the I/O.

The ADATA SU750 datasheet specifies an operating temperature range
of 0–70°C. See the [official ADATA SU750 datasheet](https://webapi3.adata.com/storage/downloadfile/datasheet_su750_25_inch_sata_ssd_20230307.pdf).
The latest observed temperature was within that published range,
but is elevated for an idle system and leaves limited margin to the
upper limit. No SMART errors or increase in the listed error counters
were observed during this check.

Operational decision: close the initial thermal investigation for now
without further stress tests or configuration changes. Continue normal
use while monitoring temperature and SMART health. Reopen the
investigation if the SSD repeatedly reaches or exceeds 70°C, SMART
indicators deteriorate, or I/O errors or device disconnects occur.

## 5. Virtualization and CPU capabilities

The CPU flags include `vmx`, indicating advertised Intel VT-x support.

The `kvm` and `kvm_intel` kernel modules are loaded. `/dev/kvm` exists,
and the KVM API responds with version 12.

### Installed virtualization stack

The following components were installed after the initial hardware audit:

- QEMU system emulator and utilities: version `10.2.1`.
- libvirt clients and system daemon: version `12.0.0`.
- `virt-install`: version `5.1.0`.

The `libvirtd` service is active and enabled. The persistent libvirt
`default` network is active and configured for automatic startup.

### Access model

Installing the libvirt driver package added the sole member of the
`sudo` group to the `libvirt` group on 2026-10-20 at approximately 13:09.
The journal records the `adduser` and `usermod` operations. The cause is
the postinstall script of `libvirt-daemon-driver-qemu`: its
`add_users_groups()` function adds every `sudo` member to `libvirt`, and
it is invoked in the `configure` step of the package.

Membership in `libvirt` allows managing virtual machines without `sudo`,
which is a high level of privilege on the host. The lab plan uses
`sudo virsh` instead.

**Remediation (2026-10-27):** the administrative account was removed from
the `libvirt` group. Verification:

- `getent group libvirt` shows no members.
- An unprivileged `virsh list --all` fails with a permission error on the
  libvirt socket.
- `sudo virsh list --all` succeeds.

Reinstalling or upgrading `libvirt-daemon-driver-qemu` runs the postinstall
script again and may restore the membership. Check group membership after
any update to that package.

### Practical VM test

A TinyCore guest was created and launched successfully. During the test,
it received a DHCP address from the default libvirt network. The guest was
removed after the test. The ISO used for the test was removed manually by
the operator.

The current `sudo virsh list --all` output shows no registered guest VMs.

Internet connectivity from inside a guest has not been verified.
These results demonstrate that a guest could be launched, but do not
establish that every virtualization workload will perform well on this
system's 6 GB of RAM.

## 6. Container runtime (Docker)

**Status:** Installed; daemon operational; functional test passed.

### Installed components

| Component | Package version | Installation type |
| --- | --- | --- |
| Docker Engine (`docker.io`) | 29.1.3-0ubuntu4.1 | Requested |
| Docker Compose plugin (`docker-compose-v2`) | 2.40.3+ds1-0ubuntu1 | Requested |
| containerd | 2.2.2-0ubuntu1.1 | Automatic (dependency) |
| runc | 1.4.0-0ubuntu1 | Automatic (dependency) |

### Installation record

The package manager recorded the installation on 2026-10-20 at
approximately 13:43 (local time) with the command:

    apt install --no-install-recommends docker.io docker-compose-v2

The APT history attributes the operation to the local administrator
account (UID 1000), and the sudo log corroborates the session. The
installation was performed during lab preparation.

### Service status

Observed on 2026-10-26 after boot:

- `containerd` started at approximately 21:58:03 and `dockerd` at 21:58:10.
- `docker.service` is active and enabled.
- `docker info` returned successfully: server version 29.1.3, `overlayfs`
  storage driver with the containerd snapshotter, cgroups v2 with the
  systemd driver, `runc` as the default runtime, and `iptables` as the
  firewall backend.
- No containers were listed, including stopped containers. One local
  image was present.

### Functional test

`hello-world:latest` (image ID `11a3eb1597e8`):

- Executed on 2026-10-20 with `sudo docker run --rm hello-world`. The
  `--rm` flag removed the container after it finished.
- Re-executed on 2026-10-26 with the same command; output included
  "Hello from Docker!".

### Privilege configuration

- The `docker` group exists and has no members.
- Docker administration currently requires `sudo`.
- Group membership has not been changed and is not authorized as part of
  this record.

### Startup warnings

Each observed start of `dockerd` logged the messages
`Deleting nftables IPv4 rules` and `Deleting nftables IPv6 rules` with
`exit status 1`. The daemon completed initialization after these
messages, and the service remained operational. The cause has not been
investigated. After startup, Docker also reports rules in the `ip` table
of nftables.

### Outstanding items

- Investigate the nftables messages logged at daemon startup.

This record does not authorize package installation, service
reconfiguration, group membership changes, container execution, or
repository publication.

## 7. Audit limitations and next checks

- SMBIOS reports four memory device entries. On 2026-10-26, two were
  populated (4 GB and 2 GB) and two reported no module. The physical
  count of two slots is consistent with this, but the reason the firmware
  reports four entries has not been established.
- SSD SMART health and temperature have been checked; see the drive
  health and thermal observations above. The source of background SSD
  writes has not been identified.
- A TinyCore guest launch was verified, but guest Internet connectivity
  and performance under heavier workloads remain untested.
- Investigate the nftables messages logged at Docker startup.
- These findings describe the system at the time of each observation
  and should be updated if the hardware or software configuration changes.
