---
tags:
  - Microsoft Azure
  - Cybersecurity
---

1. In Azure Policy, how would you apply several audit policies to multiple subscriptions in the same tenant?

    Create the audit policy definition
    Add the policies to an initiative
    Assign the initiative to a management group holding all the required subscriptions.

2. What is a gateway subnet in an Azure VNET?

    A dedicated subnet used for allocation of the virtual network gateway IP addresses.

3. What configuration changes must you make to monitor the real time attack metrics and diagnostic logs of distributed denial of service (DDoS) attacks on a public IP of your Azure Virtual Network (VNet)?

    Turn on Azure DDoS Protection for the VNet to get real-time attack metrics and diagnostic logs. (DDoS Protection Standard is called DDoS Network Protection now, and there's also a per-IP option called DDoS IP Protection.)

4. You need four /24 subnets in your Azure Virtual Network. Which address space should you select?

    172.16.0.0/22

5. When can Azure subnets have overlapping IP address spaces?

    When they're in different virtual networks that aren't connected to each other. The subscription doesn't matter. Once you try to peer them or connect them with a VPN, the address spaces can't overlap.

6. You have deployed a firewall network virtual appliance in a dedicated subnet in an Azure VNet. How do you ensure that traffic from VMs use the NVA for outbound traffic?

    Configure user-defined routing with a default route for VMs.

7. You have a stateless web application that experiences unpredictable spikes in demand. How would you approach scaling to handle this fluctuation?

    Scale out based on demand.

8. Which mechanism is used to impose forced tunneling on an Azure VNet?

    User-defined routing

9. How do you configure drive encryption for Linux in Microsoft Azure?

    Azure Disk Encryption (ADE) encrypts Linux drives with the dm-crypt feature and stores the keys in Azure Key Vault. Heads up though: ADE retires on September 15, 2028. Microsoft says to use encryption at host for new VMs instead.

10. What is the practice of sending all internet bound traffic back through your on-premises location via a site-to-site VPN?

    Forced tunneling

11. You are configuring a network security group to manage traffic between two subnets in an Azure VNet. What rule do you need to add to allow outbound communication to the internet for each subnet?

    Outbound traffic to the internet is allowed by default by the NSG (the `AllowInternetOutBound` default rule).

12. How do you enable resources to communicate with the internet from the Azure Virtual Network?

    It used to be enabled by default (called default outbound access). That's changing: new virtual networks created with API versions after March 31, 2026 get private subnets by default, so VMs need an explicit outbound method like a NAT Gateway, a public IP, or load balancer outbound rules. Existing VNets aren't affected.
