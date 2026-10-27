---
tags:
  - Microsoft Azure
  - Computer Networking
---

- _Azure virtual networks_ (VNets) let Azure resources like VMs, web apps, and databases talk to each other, to users on the internet, and to your on-prem computers.

- Azure ExpressRoute is for when you need more bandwidth and more predictable, private connectivity. It's a dedicated private connection to Azure that doesn't go over the internet.

- A point-to-site VPN is the typical way a single computer outside your organization connects back into your network. The client computer starts an encrypted VPN connection to the Azure virtual network.

- You can route traffic with route tables and border gateway protocol. Border Gateway Protocol (BGP) works with Azure VPN gateways, Azure Route Server, or ExpressRoute to propagate on-premises BGP routes to Azure virtual networks.

- Filter network traffic with network security groups (NSGs) and network virtual appliances (NVAs). An NVA is a specialized VM, kind of like a hardened network appliance, that does one network job such as being a firewall or doing WAN optimization.

- You can link virtual networks together with virtual network _peering_, so resources in each network can talk to each other.

- A VNet is in a single region and single subscription.

- Implicit FTP over SSL can't be used to create a secure communication tunnel.

- Site-to-site VPN isn't an ExpressRoute connectivity model.

- A virtual network gateway is composed of two or more special VMs that are deployed to a specific subnet.

Tips from the community:
 
- Wesley Haakman, a Principal Azure Architect and Azure MVP, makes a point worth keeping in mind: people tend to just start deploying resources in Azure or AWS, but before anything goes to production you need to think about security and isolation. That's when networking actually starts to matter.
  [Azure Networking Guide: VNets, Security & more](https://intercept.cloud/en-gb/blogs/azure-networking)

- A subnetting detail: Azure reserves five IP addresses per subnet, not one. For a subnet like 172.16.0.0/16, the first four addresses and the last one are reserved: the network address, the default gateway, two for Azure DNS, and the broadcast address.
  [Azure Networking Guide: VNets, Security & more](https://intercept.cloud/en-gb/blogs/azure-networking)
  
- Aidan Finn's take on Virtual WAN hubs: unlike a VNet-based hub, the vWAN hub VNet lives in a Microsoft-managed tenant you can't get into. You lose the ability to drop in a diagnostic VM or troubleshoot directly, and you're dependent on Azure support instead.
  [Aidan Finn, IT Pro](https://aidanfinn.com/)
