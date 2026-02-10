---
tags:
  - Azure
  - Questions
Date: 2023-08-10
---
1. In Azure Policy, how would you apply several audit policies to multiple subscriptions in the same tenant?
    
    1. Create the audit policy definitions.
    
    1. Add the policies to an initiative.
    
    1. Assign the initiative to a management group holding all the required subscriptions.
    

1. What is a gateway subnet in an Azure VNET?
    
    A dedicated subnet used for allocation of the virtual network gateway IP addresses.
    

1. What configuration changes must you make to monitor the real time attack metrics and diagnostic logs of distributed denial of service (DDoS) attacks on a public IP of your Azure Virtual Network (VNet)?
    
    Configure DDoS protection standard service for Azure VNET to monitor real time metrics and diagnostic logs.
    

1. You need four /24 subnets in your Azure Virtual Network. Which address space should you select?
    
    172.16.0.0/22
    

1. When can Azure subnets have overlapping IP address spaces?
    
    When they are in two different Azure Virtual Networks with different subscriptions.
    

1. You have deployed a firewall network virtual appliance in a dedicated subnet in an Azure VNet. How do you ensure that traffic from VMs use the NVA for outbound traffic?
    
    Configure user-defined routing with a default route for VMs.
    

1. You have a stateless web application that experiences unpredictable spikes in demand. How would you approach scaling to handle this fluctuation?
    
    Scale out based on demand.
    

1. Which mechanism is used to impose forced tunneling on an Azure VNet?
    
    User-defined routing
    

1. How do you configure drive encryption for Linux in Microsoft Azure?
    
    Linux drives are encrypted with the dm-crypt feature and keys will be stored in Azure Key Vault.
    

1. What is the practice of sending all internet bound traffic back through your on-premises location via a site-to-site VPN?
    
    Forced tunneling
    

1. You are configuring a network security group to manage traffic between two subnets in an Azure VNet. What rule do you need to add to allow outbound communication to the internet for each subnet?
    
    Outbound traffic to the internet is allowed by default.
    

1. How do you enable resources to communicate with the internet from the Azure Virtual Network?
    
    Communication is enabled by default.