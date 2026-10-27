---
tags:
  - Microsoft Azure
  - Cybersecurity
---

- Microsoft Defender for Cloud

    - Has policy and compliance metrics, a secure score to push you toward good security hygiene, and alerts for resources that aren't secure.

    - Secure score is a percentage based KPI that tells you how good (or bad) your security posture is.

    - Cloud security posture management (CSPM) is how you find and fix misconfigurations and compliance violations across a multicloud environment (Azure, AWS, GCP) before someone takes advantage of them.

    - The Defender plans (Defender for Servers, Storage, SQL, Containers, and more) add threat protection for specific workloads on top of the posture stuff.

- Microsoft Defender for Identity

    - Watches your users (their activity and info) and builds a baseline of normal behavior, so it can flag things that don't fit.

    - It maps what it sees to the stages of an attack (the cyber kill chain), like recon, lateral movement, and domain dominance.

    - It uses signals from your on-premises Active Directory to find advanced threats, compromised identities, and malicious insiders.

    - It also covers AD FS, AD CS, and Entra Connect servers, so your whole hybrid identity setup is watched and not just the domain controllers.

- Microsoft Defender for Endpoint

    - Helps you prevent, detect, investigate, and respond to threats on devices across your organization, before and after a breach.

    - Vulnerability management: finds, prioritizes, and helps you fix vulnerabilities and misconfigurations on your endpoints. This is called Microsoft Defender Vulnerability Management now.

    - Attack surface reduction: makes devices harder to attack with things like ASR rules, application control, network protection, and web protection.

    - Next-generation protection: the antivirus part. It uses behavior-based and cloud-delivered protection to catch new threats.

    - Endpoint detection and response (EDR): catches the advanced stuff that got past the earlier layers. This is also where advanced hunting (KQL against device data) and custom detections come in.

    - Automated investigation and remediation: investigates alerts and fixes issues automatically so the SOC isn't doing everything by hand.

    - Microsoft Defender Experts: Microsoft's own analysts doing managed hunting and response for you. This used to be called Microsoft Threat Experts.

    - Management and APIs: you can manage it with Intune, Group Policy, or third party tools, and its API lets you automate workflows. It plugs into Microsoft Sentinel, Defender for Cloud, and the rest of the Defender stack.

- Microsoft Defender XDR (used to be called Microsoft 365 Defender)

    - Pulls signals from all the Defender products (Endpoint, Identity, Office 365, Cloud Apps) and correlates them into one incident that tells the story of the attack. So a weird process on a laptop from Defender for Endpoint and a suspicious sign-in from Defender for Identity end up in the same incident instead of two separate alerts.

    - It all lives in the Microsoft Defender portal, which is also where Microsoft Sentinel is moving.

[Documentation | Microsoft Learn](https://learn.microsoft.com/defender-xdr/microsoft-365-defender)
