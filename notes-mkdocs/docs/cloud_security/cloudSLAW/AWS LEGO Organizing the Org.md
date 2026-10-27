---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lab

1. Organized and created OUs:
    - Infrastructure (shared services and network resources)
    - Workloads (application environments)
    - Exceptions (temporary policy exemptions)
    - Sandbox (developer experimentation)
    - Onboarding (mergers and acquisitions)
    - Nursery (new accounts before they get deployed)
    - Suspended (accounts marked for deprovisioning)
    - IncidentResponse (accounts with an active security incident)

    [Chris Farris GitHub repo that deploys OUs with Terraform](https://github.com/primeharbor/org-kickstart/blob/main/ous.tf?utm_source=slaw.securosis.com&utm_medium=referral&utm_campaign=aws-lego-organizing-the-org)

2. Created two new AWS accounts and moved them to the Security OU:
    - IAM (just for identity and access management)
    - SecurityOperations (holds security tools that can make changes)

    Why?

    - Keeping IAM in its own account isolates identity management, which cuts down on privilege escalation risk.
    - The SecurityOperations account gives security tools a controlled place to live.

## But Why?

1. Why separate OUs? To organize accounts by their security and operational needs.
2. Why does organization matter? It makes it a lot easier to enforce access control and security policies.
3. Why enforce strict access control? To limit the blast radius of a breach.
4. Why minimize the blast radius? So a compromised account or a misconfiguration does less damage.
5. Why care about misconfigurations? They're one of the top causes of cloud security incidents.
