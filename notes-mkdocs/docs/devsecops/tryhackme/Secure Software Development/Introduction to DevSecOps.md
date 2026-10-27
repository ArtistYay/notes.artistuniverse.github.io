---
tags:
  - DevOps
  - Cybersecurity
---

## The Problem with Waterfall & Rise of Agile

- Waterfall Model:
    - Sequential phases, rigid structure.
    - Difficult collaboration, blame game when issues arose.
    - Slow feedback cycles.
- Agile Methodology:
    - Values customer collaboration over contract negotiation (straight from the Agile Manifesto).
    - Self-organizing teams, constructive collaboration.
    - Iterative development, faster feedback.
    - _Key Difference:_ Focus on teamwork and flexibility.

## DevOps: The Cultural Shift

- Beyond Methodologies: DevOps is a _cultural change_ more than a process.
- Goal: Increase efficiency through trust and better communication between developers and other teams (Ops, Security, etc.).
- Key Enablers: Automation and integration are what drive this cultural change and bring teams together, which breaks down silos.

## The Infinite Loop (DevOps Lifecycle)

- CI/CD (Continuous Integration/Continuous Delivery/Deployment):
    - Frequent code merging.
    - Automated testing for new code pushes and merges.
    - _Goal:_ Quickly and reliably release changes.
- IaC (Infrastructure as Code):
    - Provisioning infrastructure through reusable, consistent code.
    - _Benefit:_ Automation, consistency, version control for infrastructure.
- Orchestration:
    - Automating complex workflows.
    - _Example:_ Container orchestration (Kubernetes).
- Monitoring:
    - Collecting data to analyze performance and stability of services.
    - _Goal:_ Proactive identification and resolution of issues.
- Microservices:
    - Breaking down applications into small, independent services.
    - _Benefit:_ Easier to develop, deploy, and scale individual parts of an application.

## Shifting Left

- Definition: Integrating security practices early in the software development lifecycle.
- _Why?_ Reduces the cost and effort of fixing security vulnerabilities later. Security becomes part of the process instead of something tacked on at the end.

## DevSecOps: Security Strikes Back

- Core Idea: Builds on DevOps by integrating security as a _shared responsibility_. Everyone on the team is responsible for security, not just a dedicated security engineer.
- Key Principles:
    - Automation: Automate security testing and processes.
    - Platform Design: Design platforms with security built-in.
    - Shared Responsibility: Breaks down security silos.
- Challenges of Traditional Security (Silos):
    - Siloed Culture: Security team isolated, leading to communication and collaboration issues.
    - Lack of Visibility: Difficult to prioritize and address the right risks at the right time.
    - Stringent Processes: Overly complicated security procedures that slow down development. This can lead to developers bypassing security altogether.
