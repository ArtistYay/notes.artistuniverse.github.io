---
tags:
  - Computer Networking
  - Microsoft Azure
---

Use gateway transit to let traffic flow from one spoke to another. Gateway transit works by adding a gateway to the hub virtual network. The hub gateway learns about the spoke subnets through the peering relationships and routes traffic between the spokes. This lab uses a VPN gateway as the routing device in the hub.

1. Created three VNets: a Hub (10.0.0.0/16), Spoke1 (10.1.0.0/16), and Spoke2 (10.2.0.0/16).

2. Deployed a virtual network gateway in the Hub VNet with two public IP addresses. The hub gateway learns about the spokes once the peering is set up.

3. Created two VMs, one in each spoke VNet.

4. Peered each spoke to the hub. On the hub side of the peering, turn on "Allow gateway transit," and on the spoke side, turn on "Use remote gateways." Peering isn't transitive, so without the gateway the two spokes can't talk to each other through the hub.

5. To get the VMs talking to each other, I had to create a route table for each spoke subnet (pointing the other spoke's address space at the hub gateway) and then associate the route table with the subnet.

6. Tested connectivity from one of the spoke VMs using ICMP (ping). The routes can take a little while to kick in.
