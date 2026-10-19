# Documentation Index

This directory contains technical records supporting the DevOps Lab, including environment assessments, implementation notes, troubleshooting reports, and operational procedures.

## Environment and Infrastructure

- [Hardware and Operating Environment](03-hardware-and-operating-environment.md) — initial hardware inventory, operating-system details, SSD/HDD health assessment, Btrfs layout, identified risks, and recovery planning.
- [Ubuntu Installation and Post-Install Verification](04-ubuntu-installation-and-post-install.md) — current Ubuntu installation, LVM layout, network configuration, boot troubleshooting, and development environment baseline.

## Project Decisions

- [Technical Decision Records](DECISIONS.md) — rationale, trade-offs, and review policy for major project decisions.

## Planned Documentation

Add documents as the corresponding work is performed:

- Clean operating-system installation and post-install verification
- Linux administration labs and troubleshooting records
- Networking and service configuration
- Backup and recovery procedures
- Docker and Docker Compose deployments
- Automation and CI/CD implementation reports

## Documentation Standard

Where applicable, each report should include:

1. **Objective** — the problem or task.
2. **Environment** — relevant hardware, operating system, and software versions.
3. **Procedure** — commands, configuration, and implementation steps.
4. **Results** — observed output and verification.
5. **Troubleshooting** — symptoms, investigation, and resolution.
6. **Security and reliability** — risks, limitations, and safeguards.
7. **Lessons learned** — conclusions and next steps.

Document only work that has actually been performed. Mark proposed procedures and unverified findings clearly. Never commit passwords, access tokens, private keys, or sensitive personal data.
