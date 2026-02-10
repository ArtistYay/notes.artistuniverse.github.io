1. What is the network address, broadcast address, valid host addresses, and subnet mask in dotted decimal notation for the IP address 198.22.45.173/26?
    
    A Class C address is 192.0.0.0 to 223.255.255.0. The default subnet mask is 255.255.255.0
    
    The default notation is /24. /26 is taking 2 bits from the host (right side of the subnet mask).
    
    Bit value of 255.255.255.0
    
    In order to get the number of subnets we have to use to the power of 2^2 = 4 subnets.
    
    Now since we are taking two bits from the host side we have to add them up, so add 128 + 64 = 192.
    
    Our subnet mask is 255.255.255.192
    
    Now we have to calculate the address range for the subnet.
    
    This is the bit value of 198.22.45.173
    
    Bit value of 255.255.255.0
    
    The network portion of the address is 26. 8+8+8+2 = 26
    
    198.22.45.128 is the network address of that subnet. If you want to know the next subnet address start add the 64 to the 128 which gives 198.22.45.192
    
    The broadcast address will be 198.22.45.191 and the valid host addresses are 198.22.45.129 to 198.22.45.190

- A process of breaking a network down into smaller subnetworks. Allows you to break it into smaller allocations for use in smaller networks.

- You can learn [here](https://youtu.be/ecCuyq-Wprc).