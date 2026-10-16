# Ubuntu Installation and Post-Install Verification

## 1. Objective

Record the clean Ubuntu installation, validate the workstation's initial
configuration, document the network startup issue and its resolution,
and establish a baseline for future DevOps labs.

## 2. Hardware and Operating System

| Property | Verified value |
|---|---|
| Laptop | VIT M2400 |
| Underlying platform | GIGABYTE E1425M |
| BIOS version | 1.02.01GB |
| BIOS date | 2011-10-20 |
| Architecture | x86-64 |
| Operating system | Ubuntu 26.04.1 LTS |
| Codename | resolute |
| Kernel | 7.0.0-38-generic |
| Desktop | XFCE |
| Default systemd target | graphical.target |
| CPU | Intel Core i3-M330 |
| Physical memory | 6 GiB installed; 5.1 GiB reported usable |
| Swap | 4 GiB |

## 3. Storage Configuration

The system uses the ADATA SU750 SSD as its primary storage device.

| Component | Filesystem/type | Capacity |
|---|---|---:|
| `/dev/sda` | ADATA SU750 SSD | 476.9 GiB |
| `/dev/sda2` | ext4, mounted at `/boot` | 2 GiB |
| `/dev/sda3` | LVM physical volume | 474.93 GiB |
| `ubuntu-vg` | LVM volume group | 474.93 GiB |
| `ubuntu-lv` | LVM logical volume | 100 GiB |
| `/` | ext4 on LVM | Approximately 98 GiB usable |

At verification time, the volume group reported 374.93 GiB of free space.
The root filesystem had approximately 84 GiB available.

The previous hardware audit identified a failing WDC HDD. That drive did not
appear as a usable storage device in the current `lsblk` output. The
available output does not establish whether the drive is physically
disconnected; verify its physical status separately if necessary.

## 4. Network Configuration

| Component | Observed state |
|---|---|
| NetworkManager | Active |
| systemd-networkd | Active |
| systemd-resolved | Active |
| Wi-Fi interface | `wlp2s0`, connected |
| Wi-Fi IPv4 address | `192.168.50.148` at verification time |
| Ethernet interface | `enp4s0`, unavailable |
| VPN interface | `proton`, WireGuard |
| Main IPv4 default route | Via `192.168.50.1` on `wlp2s0` |

NetworkManager reports Wi-Fi and the Proton WireGuard connection as active.
The main routing table alone does not establish whether all traffic is
routed through the VPN. Policy routing and VPN behavior require separate
verification.

The home router was configured to use Quad9 DNS over TLS. After that
configuration, the user reported being able to reach the Proton VPN domain.
This is an observed improvement, not proof that DNS was the only filtering
mechanism involved.

## 5. Boot Troubleshooting

### Problem

During startup, the system spent approximately two minutes waiting for
`systemd-networkd-wait-online.service`, which then failed with a timeout.

### Investigation

The following services were active:

- NetworkManager
- systemd-networkd
- systemd-resolved

NetworkManager managed the Wi-Fi connection. `networkctl list` showed the
network interfaces as unmanaged by systemd-networkd.

The wait-online unit timed out while waiting for network connectivity.

### Change and verification

The wait-online unit was disabled:

```bash
sudo systemctl disable systemd-networkd-wait-online.service
```

After reboot, the measured startup time was approximately 20.6 seconds.
The graphical target was reached, and `systemctl --failed` reported no
failed units.

The wait-online unit was disabled because NetworkManager managed the
Wi-Fi connection and the interfaces were unmanaged by systemd-networkd.
The systemd-networkd service itself remains active.

### Boot verification

Observed results after reboot:

- Kernel: approximately 3.2 seconds.
- Initrd: approximately 2.8 seconds.
- Userspace: approximately 14.6 seconds.
- Total startup time: approximately 20.6 seconds.
- Failed systemd units: zero.

These measurements are a baseline and may vary between boots.

## 6. Development Environment Baseline

| Component | Observed version or state |
|---|---|
| Git | 2.53.0 |
| Python | 3.14.4 |
| Bash | 5.3.9 |
| curl | 8.18.0 |
| Python pip module | Not available through the current Python installation |
| Python venv support | Available |
| Docker CLI | Not found during the initial check |
| Visual Studio Code CLI | Not found during the initial check |
| Git author identity | Not configured at the time of the audit |

The absence of a command during the initial check does not establish that
the corresponding software cannot be installed.

The package index update completed successfully. At the initial check,
18 packages were reported as upgradable. A subsequent package upgrade was
run, and no reboot-required flag was reported at the last verification.

## 7. Security and Operational Notes

- Do not store passwords, VPN configuration secrets, access tokens, or
  private keys in this repository.
- Continue using the SSD as the primary storage device.
- Do not rely on the previously failing WDC HDD for important data.
- Verify the VPN routing and DNS behavior separately instead of assuming
  that an active VPN connection carries all traffic.
- Prefer project-specific Python virtual environments over installing
  Python packages globally with `sudo pip`.

## 8. Follow-Up Checklist

- [x] Install Ubuntu and establish the initial system baseline.
- [x] Investigate and mitigate the boot wait-online timeout.
- [ ] Verify VPN routing, DNS, and public IP behavior.
- [x] Configure Git author identity for this repository.
- [ ] Install and verify the required development tools.
- [ ] Create the first reproducible Linux administration lab.
- [ ] Record commands, results, and troubleshooting evidence.
