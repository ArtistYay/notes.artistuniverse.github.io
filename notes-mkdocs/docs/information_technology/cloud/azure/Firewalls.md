---
tags:
  - Microsoft Azure
  - Computer Networking
---

- A device that historically sits at the border between different networks and monitors traffic flowing between them.

- It's capable of reading packet data and either allowing or denying traffic based on that data.

- Firewalls establish a barrier between networks of different security levels.

- What a firewall can read and act on depends on which OSI layer it works at. A layer 3 firewall can act on source and destination IP addresses and ranges. Layer 4 adds protocols and port numbers. A stateful firewall also tracks connections, so it knows which traffic is a response to something that went out. Layer 7 firewalls understand the application itself (like URLs or app-specific commands).

Tips from the community:
 
- Aidan Finn's hub design pattern: put a small diagnostic VM in the hub next to the firewall. If a connection is failing, you can test from that VM to prove quickly whether the firewall is actually the problem, without touching production traffic.
  [Aidan Finn, IT Pro](https://aidanfinn.com/)

- Worth knowing as a limitation, not a tip exactly: in a Virtual WAN hub, the hub VNet sits in a Microsoft-managed tenant. You can't get into it to troubleshoot, which means you're at the mercy of Azure support if something's wrong at the hub level. That's not true of a VNet-based hub, where you have full access.
  [Aidan Finn, IT Pro](https://aidanfinn.com/)
