---
tags:
  - Azure
Keyword: Networking
---
- An Azure VPN gateway is a specific type of virtual network gateway that is used to send and receive encrypted traffic between an Azure virtual network and an on-premises location over the public Internet.

- You can only deploy only one VPN gateway in each VNet but can use one gateway to connect to multiple locations.

- They are two types of VPN types. policy based and route based.

- Policy-based VPN gateways specify statically the IP address of packets that should be encrypted through each tunnel. This type of device evaluates every data packet against those sets of IP addresses to choose the tunnel where that packet is going to be sent through.

- With route-based gateways, IPSec tunnels are modeled as a network interface or virtual tunnel interface. IP routing (either static routes or dynamic routing protocols) decides which one of these tunnel interfaces to use when sending each packet. Route-based VPNs are the preferred connection method for on-premises devices. They're more resilient to topology changes such as the creation of new subnets.

- VPN gateways use a pre-shared key as the only method of authentication. Both types also rely on Internet Key Exchange (IKE) in either version 1 or version 2 and Internet Protocol Security (IPSec). IKE is used to set up a security association (an agreement of the encryption) between two endpoints. This association is then passed to the IPSec suite, which encrypts and decrypts data packets encapsulated in the VPN tunnel.

- A virtual network gateway is composed of two or more virtual machines that are deployed to a specific subnet you create which is called the gateway subnet.

- A VPN Gateway is a specific to of virtual network gateway that is used to send encrypted traffic between an Azure virtual network and an on-premises location over the public internet.