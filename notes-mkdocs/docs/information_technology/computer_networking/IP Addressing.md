- IPv4 addresses are how two devices can communicate at layer 4 and above of OSI seven layer model.

- They are 32-bit binary values but are represented in dotted decimal notation to make them easier for humans to read and understand.

- Each octet is made up of 1 byte and 8 bits.

- IPs are split into a network part and a node or host part. The netmask (255.255.255.0) or prefix (/24) shows where this split occurs.

- 0.0.0.0 and 0.0.0.0/0 represents all IP addresses.

- 255.255.255.255 is the IP address used to broadcast to all addresses everywhere but was later filtered so it can not be passed between networks.

- 127.0.0.1 is a [localhost](http://localhost) or loopback address. Whatever the IP address of the device you are using, it can be referenced by itself as 127.0.0.1. So a web server on your laptop will be 127.0.0.1:80.

- 169.254.0.1 to 169.254.255.254 is a range of IP addresses that a device can auto configure with if it’s using DHCP and fails to automatically get an IP from a DHCP server.

- Class A (/8) is 1.0.0.0 to 126.255.255.255. It has 126 networks and 16,777,214 hosts (nodes) in each. 2 IPs are reserved.

- Class B (/16) is 128.0.0.0 to 191.255.255.255. It has 16,382 networks and 65,534 hosts (nodes) in each. 2 IPs are reserved.

- Class C (/24) is 192.0.0.0 to 223.255.255.255. It has 2,097,150 networks and 254 hosts (nodes) in each. 2 IPs are reserved.

- Private networking IPs
    
    - IP classes have a number of ranges within them used for private networking only.
    
    - Class A has range 10.0.0.0 to 10.255.255.255
    
    - Class B has range 172.16.0.0 to 172.32.255.255
    
    - Class C has range 192.168.0.0 to 192.168.255.255
    

- [CIDR](https://cidr.xyz/) (Classless Inter-Domain Routing) is used for IPv4 IP networking rather then the class system. It allows more effective allocation and subnetworking.

- The network address is your starting point. The prefix is the number of bits the network uses, the remaining bits, and the node part is yours to use. The node (host) part is yours from all 0’s to all 1’s.