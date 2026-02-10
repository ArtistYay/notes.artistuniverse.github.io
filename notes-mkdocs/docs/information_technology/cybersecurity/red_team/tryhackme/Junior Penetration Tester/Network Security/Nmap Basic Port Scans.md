### **I. TCP and UDP Ports**

Ports are the communication endpoints for network services. TCP and UDP are the two main transport protocols.

- **TCP:** Connection-oriented, reliable, ordered delivery. Used for applications that require guaranteed data delivery (e.g., web browsing, file transfer).
    
- **UDP:** Connectionless, unreliable, unordered delivery. Used for applications where speed is more important than reliability (e.g., streaming video, online games).
    
- **Nmap Port States:** Nmap categorizes ports into six states:
    
    1. **Open:** A service is actively listening on the port.
        
    2. **Closed:** The port is accessible, but no service is listening. This usually means the port is intentionally closed.
        
    3. **Filtered:** Nmap cannot determine the port state due to a firewall or other network filtering. The port might be open or closed, but Nmap can't reach it.
        
    4. **Unfiltered:** Nmap can reach the port, but cannot determine if it is open or closed. This state is specific to ACK scan (`-sA`) results.
        
    5. **Open|Filtered:** Nmap thinks the port is either open or filtered, but can't be more specific.
        
    6. **Closed|Filtered:** Nmap thinks the port is either closed or filtered, but can't be more specific.
### **II. TCP Flags**

TCP flags are control bits within the TCP header that manage connections.

- **URG (Urgent):** Signals that the data is urgent and should be processed immediately.
    
- **ACK (Acknowledgment):** Acknowledges the receipt of data. Essential for reliable communication.
    
- **PSH (Push):** Tells the receiving application to deliver the data immediately, rather than buffering it.
    
- **RST (Reset):** Terminates a connection abruptly. Can be used by firewalls or when a connection attempt is made to a closed port.
    
- **SYN (Synchronize):** Used to initiate the TCP 3-way handshake (SYN, SYN-ACK, ACK), which establishes a connection.
    
- **FIN (Finish):** Signals that the sender has no more data to send, used to gracefully close a connection.
### **III. TCP Connect Scan (-sT)**

The TCP connect scan is the most basic TCP scan type.

- **Full 3-Way Handshake:** It completes the full TCP 3-way handshake. This makes it less stealthy than other scan types, as it leaves a clear record of the connection attempt.
    
- **Unprivileged Users:** It's the only TCP scan available to unprivileged users (those without root or administrator access).
    
- **`-F` (Fast Mode):** Scans only the 100 most common ports, instead of the default 1000.
    
- **`-r`:** Scans ports sequentially, rather than randomly. Useful for testing port behavior over time.
### **IV. TCP SYN Scan (-sS)**

The SYN scan is the default and most common TCP scan.

- **Half-Open Connection:** It doesn't complete the 3-way handshake. Instead, it sends a SYN packet and, if it receives a SYN-ACK, it sends an RST to tear down the connection. This makes it more stealthy than a connect scan.
    
- **Privileged Users:** Requires root or administrator privileges.
    
- **Stealthier:** Less likely to be logged than a connect scan.
    ![screenshot](../../../images/Pasted image 20250109123545.png)

### **V. UDP Scan (-sU)**

The UDP scan is used to discover open UDP ports.

- **ICMP Port Unreachable:** If a UDP packet is sent to a closed port, the target sends back an ICMP Port Unreachable message.
    
- **Open Ports:** Ports that don't respond are considered open. UDP scans can be slow and unreliable due to the connectionless nature of UDP.
    
- **`-v` (Verbose):** Provides progress updates during the scan.
    ![screenshot](../../../images/Pasted image 20250109124713.png)
  
### **VI. Fine-Tuning Scope and Performance**

Nmap offers many options to customize scans.

- **`-p` (Port Specification):** Specifies the ports to scan.
    
    - `-p 80`: Scan port 80.
    - `-p 22-443`: Scan ports 22 through 443.
    - `-p-`: Scan all 65535 ports.
- **`--top-ports <number>`:** Scan the most common ports.
    
- **`-T<0-5>` (Timing Templates):** Controls scan speed and aggression.
    
    - `0 (Paranoid)`: Slowest, avoids detection.
    - `1 (Sneaky)`: Slow, less detectable.
    - `2 (Polite)`: Slower, reduces load on the target.
    - `3 (Normal)`: Default speed.
    - `4 (Aggressive)`: Faster, more likely to be detected.
    - `5 (Insane)`: Fastest, very likely to be detected and can be inaccurate.
- **`--min-rate <number>` and `--max-rate <number>`:** Control the number of packets sent per second.
    
- **`--min-parallelism <numprobes>` and `--max-parallelism <numprobes>`:** Control the number of probes run in parallel for host discovery and port scanning. Increasing parallelism can speed up scans but also increase the load on the network and target.

Choosing the right scan type and tuning options depends on your goals and the target environment. Consider the trade-off between speed, stealth, and accuracy. `-T4` is common for CTFs and practice, while `-T1` is often preferred for real-world engagements where stealth is important.