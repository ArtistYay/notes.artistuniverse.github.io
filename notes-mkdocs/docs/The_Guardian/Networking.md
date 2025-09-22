!!! warning
    When trying to delete an SDN zone and you get a *delete sdn zone object failed: zone PFNET is used by vnet PFSENSE at /usr/share/perl5/PVE/Network/SDN/Zones/Plugin.pm line 139. (500)* error message, you have to delete the subnet then the gateway, in order to delete the zone.
    [Link explaining](https://forum.proxmox.com/threads/sdn-cant-delete-vnet.124635/)

*Why did I choose Linux bridge(s) over OVS Bridge(s)?* The set up is more simpler in my case. Not looking for OpenFlow, VXLAN, and STT anytime soon. 

- Created three vlans, one for each Active Directory tier.

- In pfSense I created the interface assignment for each vlan and enabled the DHCP server on each.