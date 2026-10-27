---
tags:
  - Microsoft Azure
  - Compute
---

- Azure App Service lets you build, deploy, and scale web apps, mobile back ends, background jobs, and RESTful APIs in pretty much whatever language you want, without managing the infrastructure underneath. It has automatic scaling and high availability built in.

- It's a PaaS

- You can create a web app with the portal, Azure CLI, PowerShell, or ARM/Bicep templates.

- Has integrated load balancing.

- The pricing tier (plan) decides how much compute you get and how isolated it is:

    - Shared and dedicated tiers (multitenant and not deployed into your VNet, but Basic and up can use VNet integration):

        - Free and Shared (F1, D1): run on VMs shared with other customers. Fine for testing, no SLA.

        - Basic (B1, B2, B3): dedicated VMs, good for dev/test.

        - Standard (S1, S2, S3): the starting point for production. You pay per instance, and you get autoscale and deployment slots.

        - Premium v2 (P1v2, P2v2, P3v2)

        - Premium v3 (P0v3, P1v3, P2v3, P3v3, plus memory-optimized P1mv3 and up)

        - Premium v4 (the newest Premium tier)

    - Isolated v2: runs in an App Service Environment v3 (ASE), a fully dedicated environment deployed right into your own VNet, so it's exclusive to you. Since it's in your VNet, apps can reach on-prem resources over your VPN or ExpressRoute. (The older ASE v1/v2 and the original Isolated tier are retired.)

Tips from the community:
 
- Robert Smit, a Hybrid Cloud & Azure MVP, has a governance point worth pairing with any migration notes: lift-and-shift looks cheap at first, but without a governance framework it tends to produce unmanaged resources, inconsistent naming, and security that's reactive instead of planned.
  [Robert Smit MVP Blog](https://robertsmit.wordpress.com/)