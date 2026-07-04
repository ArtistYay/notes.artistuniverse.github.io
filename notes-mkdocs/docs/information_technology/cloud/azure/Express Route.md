---
tags:
  - Microsoft Azure
  - Computer Networking
---

- ExpressRoute provides private connectivity, but it isn't encrypted.

- Good fit for data that needs to be on-premises and on Azure, highly available, and periodically migrated.

- Doesn't go over the public internet.

- A private, secure, high-bandwidth, low-latency connection from your data center or infrastructure to Azure.

**Tips from the community:**
 
Aidan Finn's blog (he's a longtime Azure MVP) is probably the single best ongoing source for ExpressRoute design details that don't show up in the docs:
 
- ExpressRoute gateways can't do NAT, unlike VPN gateways. If a third party insists on a NAT'd connection over ExpressRoute, you have to build it yourself with a network virtual appliance and user-defined routes.
  [ExpressRoute | Aidan Finn, IT Pro](https://aidanfinn.com/?tag=expressroute)

- You don't need a separate circuit per hub. ExpressRoute Standard supports up to 10 simultaneous connections to virtual network gateways; Premium supports up to 100. Connections into a Virtual WAN hub have to use Premium.
  [Virtual Network Gateway | Aidan Finn, IT Pro](https://aidanfinn.com/?tag=virtual-network-gateway)

- The old "big company uses ExpressRoute, small company uses VPN" rule is too simple. The real question is whether you need a guaranteed SLA or genuinely low latency. Plenty of organizations are fine on VPN for HTTPS-based access to Azure.
  [Introduction to Azure ExpressRoute | Aidan Finn, IT Pro](https://aidanfinn.com/?p=22267)

