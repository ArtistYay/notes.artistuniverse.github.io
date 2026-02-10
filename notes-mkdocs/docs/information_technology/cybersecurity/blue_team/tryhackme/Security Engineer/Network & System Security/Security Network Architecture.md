### I. Network Segmentation

- **Purpose:** Dividing a network into smaller, isolated segments to improve security and performance.
- **VLANs (Virtual LANs):**
    - Layer 2 segmentation.
    - Differentiate devices and control traffic flow.
    - Implemented using 802.1q tags on frames.
    - **Native VLAN:** Untagged traffic on a trunk port.
- **ROAS (Router on a Stick):**
    - A router connected to a switch with a trunk port.
    - Routes traffic between different VLANs.
### II. Common Secure Network Architecture

- **Hierarchical Design:**
    - **Core Layer:** High-speed backbone, connects different parts of the network.
    - **Distribution Layer:** Provides routing, filtering, and segmentation.
    - **Access Layer:** Connects end devices to the network.
    ![[Pasted image 20240925182419.png]]
- **Security Zones:**
    - **DMZ (Demilitarized Zone):** A separate network segment for publicly accessible servers.
    - **Internal Network:** The protected internal network.
    - **Guest Network:** Isolated network for guests.
    ![[Pasted image 20240925182446.png]]
### III. Network Security Policies and Controls

- **Purpose:** Define rules and guidelines for network traffic flow and access control.
- **ACLs (Access Control Lists):**
    - **Purpose:** Filter traffic based on criteria like source/destination IP, port, protocol.
    - **Stateless:** Each packet is evaluated independently.
    - **ACE (Access Control Entry):** A single rule in an ACL.
### IV. Zone-Pair Policies & Filtering

- **Purpose:** Enforce security policies between different zones (e.g., DMZ to internal network).
- **Stateful:** Maintains information about the state of connections, allowing more granular control.
- **Direction-based:** Policies can be applied differently for different traffic directions.
### V. Validating Network Traffic

- **SSL/TLS Inspection:**
    - **Purpose:** Decrypt and inspect SSL/TLS traffic to identify threats and enforce policies.
    - **SSL Proxy:** Intercepts and decrypts SSL/TLS traffic.
    - **UTM (Unified Threat Management):** Performs deep inspection of decrypted traffic (web filtering, intrusion prevention, etc.).
### VI. Addressing Common Attacks

- **DHCP Snooping:**
    - **Purpose:** Prevent rogue DHCP servers and mitigate DHCP-related attacks.
    - **Layer 2:** Operates on switches.
    - **DHCP Binding Database:** Stores information about legitimate DHCP leases.
    - **Functions:**
        - Filters DHCP packets from untrusted sources.
        - Verifies MAC addresses.
        - Rate-limits DHCP traffic.
- **Dynamic ARP Inspection:**
    - **Purpose:** Prevent ARP spoofing and poisoning attacks.
    - **Layer 2:** Operates on switches.
    - **Functions:**
        - Validates ARP packets.
        - Intercepts and discards invalid ARP packets.
        - Uses the DHCP binding database to verify IP-to-MAC mappings.