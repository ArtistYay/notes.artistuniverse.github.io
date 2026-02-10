---
tags:
  - Azure
Keyword: Networking
---
- _Azure virtual networks_ enable Azure resources, such as VMs, web apps, and databases, to communicate with each other, with users on the internet, and with your on-premises client computers.

- Azure ExpressRoute are for environments where you need greater bandwidth and even higher levels of security. ExpressRoute provides a dedicated private connectivity to Azure that doesn't travel over the internet.

- Point-to-site virtual private network is the typical approach to a virtual private network (VPN) connection is from a computer outside your organization, back into your corporate network. In this case, the client computer initiates an encrypted VPN connection to connect that computer to the Azure virtual network.

- You can route traffic with route tables and border gateway protocol. Border Gateway Protocol (BGP) works with Azure VPN gateways, Azure Route Server, or ExpressRoute to propagate on-premises BGP routes to Azure virtual networks.

- Filter network traffic with network security groups and network virtual appliances. A network virtual appliance is a specialized VM that can be compared to a hardened network appliance. A network virtual appliance carries out a particular network function, such as running a firewall or performing wide area network (WAN) optimization.

- You can link virtual networks together by using virtual network _peering._ Peering enables resources in each virtual network to communicate with each other.

- A VNet is in a single region and single subscription.

- Implicit FTP over SSL can’t be used to create a secure communication tunnel

- Site-to-site VPN isn’t a ExpressRoute model.

- A virtual network gateway is composed of two or more special VMs that are deployed to a specific subnet.