---
tags:
  - Computer Networking
---

1. What is the network address, broadcast address, valid host addresses, and subnet mask in dotted decimal notation for the IP address 198.22.45.173/26?

    A Class C address is 192.0.0.0 to 223.255.255.255, and the default subnet mask is 255.255.255.0.

    The default notation is /24. /26 borrows 2 bits from the host side (the right side of the subnet mask).

    Bit value of 255.255.255.0

    To get the number of subnets, do 2 to the power of the borrowed bits: 2^2 = 4 subnets.

    Since we're borrowing the first two bits of the last octet, add up their values: 128 + 64 = 192.

    Our subnet mask is 255.255.255.192

    Now we calculate the address range for the subnet.

    This is the bit value of 198.22.45.173

    Bit value of 255.255.255.0

    The network portion of the address is 26 bits: 8 + 8 + 8 + 2 = 26.

    Each /26 subnet is 64 addresses (256 / 4), so the subnets start at .0, .64, .128, and .192. 173 falls between 128 and 191, so 198.22.45.128 is the network address. The next subnet starts at 128 + 64 = 198.22.45.192.

    The broadcast address is 198.22.45.191 (one before the next subnet), and the valid host addresses are 198.22.45.129 to 198.22.45.190.

- Subnetting is breaking a network down into smaller subnetworks, so you can hand out smaller chunks to smaller networks.

- You can learn more [here](https://youtu.be/ecCuyq-Wprc).
