---
tags:
  - Microsoft Azure
  - Computer Networking
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

**Tips from the community:**
 
- Wesley Haakman, a Principal Azure Architect and Azure MVP, makes a point worth keeping in mind: people tend to just start deploying resources in Azure or AWS, but before anything goes to production you need to think about security and isolation. That's when networking actually starts to matter.
  [Azure Networking Guide: VNets, Security & more](https://intercept.cloud/en-gb/blogs/azure-networking)

- A subnetting detail: Azure reserves five IP addresses per subnet, not one. For a subnet like 172.16.0.0/16, the first four addresses and the last one are reserved, one for the virtual router/default gateway, the rest for Azure's own SDN platform services.
  [Azure Networking Guide: VNets, Security & more](https://intercept.cloud/en-gb/blogs/azure-networking)
  
- Aidan Finn's take on Virtual WAN hubs: unlike a VNet-based hub, the vWAN hub VNet lives in a Microsoft-managed tenant you can't get into. You lose the ability to drop in a diagnostic VM or troubleshoot directly, and you're dependent on Azure support instead.
  [Aidan Finn, IT Pro](https://aidanfinn.com/)
