---
tags:
  - Computer Networking
---

- IPv4 addresses are how devices find each other across networks. IP lives at layer 3 (network) of the OSI seven layer model.

- They're 32-bit binary values, but we write them in dotted decimal notation so humans can actually read them.

- Each octet is 8 bits (1 byte), and there are 4 octets.

- IPs are split into a network part and a node (host) part. The netmask (255.255.255.0) or prefix (/24) shows where that split happens.

- 0.0.0.0/0 means all IP addresses (you'll see it in route tables and firewall rules a lot).

- 255.255.255.255 is the limited broadcast address. It goes to every device on your local network, but routers don't forward it, so it never leaves the network.

- 127.0.0.1 is the [localhost](http://localhost) or loopback address (the whole 127.0.0.0/8 range is loopback). No matter what IP your device has, it can always reach itself at 127.0.0.1. So a web server on your laptop is at 127.0.0.1:80.

- 169.254.0.0/16 is the link-local (APIPA) range. If a device is set to use DHCP and can't get an address from a DHCP server, it gives itself one in this range. Seeing a 169.254.x.x address is usually your first clue DHCP is broken.

- Class A (/8) is 1.0.0.0 to 126.255.255.255. It has 126 usable networks and 16,777,214 hosts in each (2 IPs per network are reserved for the network and broadcast addresses).

- Class B (/16) is 128.0.0.0 to 191.255.255.255. It has 16,384 networks and 65,534 hosts in each.

- Class C (/24) is 192.0.0.0 to 223.255.255.255. It has 2,097,152 networks and 254 hosts in each.

- Private networking IPs (RFC 1918)

    - Each class has a range set aside for private networks only. These aren't routed on the public internet.

    - Class A range: 10.0.0.0 to 10.255.255.255 (10.0.0.0/8)

    - Class B range: 172.16.0.0 to 172.31.255.255 (172.16.0.0/12)

    - Class C range: 192.168.0.0 to 192.168.255.255 (192.168.0.0/16)

- [CIDR](https://cidr.xyz/) (Classless Inter-Domain Routing) is what IPv4 networking actually uses now instead of the class system. It lets you allocate and subnet networks way more efficiently.

- The network address is your starting point. The prefix is the number of bits the network uses, and the remaining bits are the node part, which is yours to use, from all 0's to all 1's.
