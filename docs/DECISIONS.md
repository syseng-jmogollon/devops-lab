# Technical Decision Records

This document records the major technical decisions for the DevOps Lab.
Each record describes the context, the decision, its rationale, and its
known consequences or limitations.

Decisions reflect the project's state when recorded. Revisit them when
new evidence, hardware changes, or project requirements justify doing so.

## ADR-001: Use Ubuntu 26.04.1 LTS with XFCE

**Status:** Accepted

### Context

The project needs a Linux workstation for DevOps learning, automation,
containerization, infrastructure tooling, and a future self-hosted
automation platform for the LED automotive lighting store.

Fedora was initially considered because the project owner is interested
in the Red Hat ecosystem. Ubuntu was recommended as an alternative
because of its LTS support model, broad documentation and community,
and the option to use a lightweight desktop environment.

Ubuntu 24.04 LTS was initially considered. The project owner selected
Ubuntu 26.04.1 LTS to use the newer release.

### Decision

Use Ubuntu 26.04.1 LTS with XFCE on the VIT M2400 laptop.

### Rationale

- Provides a Linux environment for practical DevOps exercises.
- Offers extensive community documentation and ecosystem support.
- XFCE provides a graphical desktop while keeping the environment
  relatively lightweight.
- Allows the same machine to serve as a workstation and a learning lab.

### Consequences and limitations

- The project owner prefers the Fedora/Red Hat ecosystem, so Fedora
  remains a relevant alternative for future evaluation.
- Choosing a newer release does not automatically make it more stable
  or more suitable for every tool. Compatibility must be verified.
- The laptop has 6 GB of installed RAM and an Intel Core i3-M330
  processor. Resource-heavy workloads may require optimization or
  an external host.
- Reconsider this decision if reproducible technical problems or
  project requirements justify a change. Do not reinstall solely
  because another distribution is available.

## ADR-002: Use the VIT M2400 as the initial lab workstation

**Status:** Accepted

### Context

The project owner has an existing VIT M2400 laptop available for
hands-on learning and experimentation. Its hardware is limited compared
with a modern development workstation.

### Decision

Use the VIT M2400 as the initial workstation and lab host rather than
making a new computer purchase a prerequisite for starting the project.

### Rationale

- Makes use of available hardware.
- Enables practical Linux administration and automation exercises.
- Keeps initial project costs low.
- Provides a real environment in which to document resource limits
  and operational trade-offs.

### Consequences and limitations

- The laptop has 6 GB of installed RAM and an Intel Core i3-M330
  processor (2 cores and 4 threads).
- Workloads must be introduced incrementally and monitored.
- Running multiple virtual machines or resource-intensive services
  concurrently may not be practical.
- Measure actual resource usage before deciding whether to upgrade
  RAM or move workloads to another host.

## ADR-003: Keep the ADATA SSD and remove the failed WDC HDD

**Status:** Accepted

### Context

The initial storage audit identified an ADATA SU750 512 GB SSD and
a WDC 320 GB HDD. The HDD reported serious SMART failure indicators,
including reallocated, pending, and uncorrectable sectors.

The project owner subsequently confirmed that the WDC HDD was
physically removed from the laptop. The SSD passed the SMART check
recorded during the initial audit.

### Decision

Use the ADATA SU750 SSD for the installed operating system and lab.
Keep the failed WDC HDD out of service.

### Rationale

- Avoids relying on a drive that reported serious failure indicators.
- Keeps the active lab installation on the SSD.
- Reduces the risk of accidental use of the failed HDD.

### Consequences and limitations

- The historical HDD SMART results are evidence from the initial audit,
  not current measurements of a drive still installed in the laptop.
- A prior SMART PASS does not guarantee that an SSD cannot fail.
- Maintain separate backups of important data and verify that backups
  are readable.

## ADR-004: Prefer free and open-source tools

**Status:** Accepted as a project preference

### Context

The project combines professional development and automation for a
small business. Recurring costs should be minimized where practical,
and the lab should be reproducible.

### Decision

Prefer free and open-source tools when they meet the functional,
security, maintainability, and learning requirements.

### Rationale

- Reduces software licensing and subscription costs.
- Supports learning through inspectable configuration and code.
- Helps document reproducible environments.
- Fits the project's preference for self-hosted automation where
  that approach is practical.

### Consequences and limitations

- Free software is not necessarily cost-free to operate or maintain.
- Self-hosted systems require attention to security, backups, updates,
  availability, and ongoing administration.
- A paid service may still be appropriate when it provides a material
  advantage in reliability, support, security, or total cost of ownership.

## Review policy

These records document decisions and their rationale; they do not
replace implementation evidence.

When a decision changes, update the relevant record with the new
status and rationale, or add a new record when preserving the history
is important. Verify technical claims against the actual environment
before treating them as established facts.
