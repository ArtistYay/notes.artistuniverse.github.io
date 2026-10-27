---
tags:
  - Cybersecurity
  - Identity & Access Management
---

The default authentication protocol for Active Directory. You basically log in once. The Key Distribution Center (KDC) on the domain controller gives you a Ticket Granting Ticket (TGT). When you want to access a file server, you trade the TGT for a service ticket for that server and show that. Your password never gets sent across the network.