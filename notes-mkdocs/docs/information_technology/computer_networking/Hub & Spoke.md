---
tags:
  - Azure
Date: 2023-08-14
---
Use a gateway transit connection to allow network traffic to flow from one spoke to another. Gateway transit works by adding a gateway to the hub virtual network. The gateway on the hub learns about the spoke subnets through the peering relationships. The VNET gateway routes traffic between each spoke creating the gateway transit relationship. This example uses a VPN gateway as the routing device in the hub.

1. Create three VNETs. A Hub (10.0.0.0/16), Spoke1 (10.1.0.0/16), and Spoke2 (10.2.0.0/16)

1. Deployed a Virtual Network Gateway in the Hub VNET with two public IP addresses. The gateway on the hub learns about the spokes establishing a peering relationship.

1. Created two VMs one in each spoke VNET.

1. Made a VNET peering to my hub from my spokes.

---
1. To enable communication between the VMs I had to create a route table for each Spoke subnet. Then associate the route table to the subnet.

---

This is the route table for spoke 1. Any traffic for spoke 2 goes to the hub.

1. Tested connectivity in one of the VMs in the spoke using ICMP. Routes may take a while to kick in.
