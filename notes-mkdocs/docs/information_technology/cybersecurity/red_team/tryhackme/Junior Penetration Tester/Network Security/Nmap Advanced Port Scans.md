### **I. Advanced Scan Types**

These scans manipulate TCP flags, the control bits within TCP packets, to elicit responses from target ports. The goal is to determine port states (open, closed, filtered) and sometimes bypass firewalls.

- **Null Scan (-sN):** Sends a packet with _no_ flags set. It's stealthy because it doesn't resemble a typical connection attempt. However, it's easily blocked by stateful firewalls. Open/filtered ports won't respond, while closed ports should send an RST (reset) packet. The "open|filtered" result means Nmap can't definitively say if the port is open or blocked by a firewall.
    
- **FIN Scan (-sF):** Sends a packet with only the FIN (finish) flag set. Similar to the Null scan, it's stealthy but vulnerable to stateful firewalls. The interpretation of responses is the same as the Null scan.
    
- **Xmas Scan (-sX):** Sets the FIN, PSH (push), and URG (urgent) flags – hence the name, like Christmas lights. It's also stealthy and has the same response interpretation as Null and FIN scans. Less reliable on Windows hosts.
    
- **Maimon Scan (-sM):** Sets the FIN and ACK flags. Historically, some BSD-derived systems would respond differently to this scan on open ports, but this is rare today. Most modern systems treat it like a Null/FIN/Xmas scan.
    
- **ACK Scan (-sA):** Sends a packet with only the ACK flag set. Crucially, _all_ ports, whether open or closed, should respond with an RST. This scan is _not_ used to directly find open ports. Instead, it's used to map firewall rules. If a firewall _doesn't_ block the ACK packet, the port is marked "unfiltered," suggesting the firewall isn't blocking that traffic. This helps identify which ports a firewall is _not_ filtering, but it doesn't mean a service is running on those ports.
    
- **Window Scan (-sW):** Similar to the ACK scan, it sends an ACK packet. However, it analyzes the TCP Window field in the RST responses. Some systems provide different window sizes for open and closed ports, allowing for differentiation. Like the ACK scan, it's more useful for firewall mapping than direct port discovery.
    
- **Custom Scan (--scanflags):** Allows you to craft a TCP packet with any combination of flags. This is for advanced users who understand the nuances of TCP flag behavior and want to experiment.
### **II. Spoofing and Decoys**

These techniques aim to make your scans harder to trace or attribute to you.

- **IP Spoofing (-S):** Makes Nmap use a fake source IP address. The target replies to the spoofed address, so you need to be able to capture those responses (e.g., if you're on the same network or have a way to route the traffic). It's often used with other techniques like idle scans.
    
- **MAC Spoofing (--spoof-mac):** Changes the source MAC address of your scan packets. This is only effective on the local network (same Ethernet or Wi-Fi). It can help hide your real MAC address from network monitoring.
    
- **Decoy Scan (-D):** Makes it appear as if the scan is coming from multiple IP addresses, including your own. This dilutes the trace and makes it harder to pinpoint the actual source of the scan. You can specify specific decoy IPs or use "RND" for random IPs.
### **III. Firewall and IDS Evasion**

Firewalls and Intrusion Detection Systems (IDS) try to detect malicious network activity. These techniques try to evade detection.

- **Fragmented Packets (-f):** Breaks down the TCP header into smaller IP fragments. The idea is that some firewalls or IDS might have trouble reassembling the fragments and therefore miss the malicious payload. `-f` fragments into 8-byte chunks, `-ff` into 16-byte chunks.
    
- **Data Length (--data-length):** Adds random data to the end of your packets, making them larger and potentially less suspicious. The goal is to blend your scan traffic with normal network traffic.
### **IV. Idle/Zombie Scan (-sI)**

This is a very stealthy technique. It uses a third, "idle" host (the zombie) to indirectly scan the target.

1. **Initial Probe:** You probe the zombie host to get its current IP ID (a number that increments with each packet sent).
    
2. **Spoofed Probe:** You send a SYN packet to the target, but you spoof the source IP address to be the zombie's IP.
    
3. **Zombie Reaction (Open Port):** If the target port is open, it sends a SYN/ACK back to the zombie. The zombie, not expecting this, responds with an RST, incrementing its IP ID.
    
4. **Zombie Reaction (Closed Port):** If the target port is closed, it sends an RST to the zombie. The zombie may or may not increment its IP ID (depending on the OS and if it considered the RST part of an established connection).
    
5. **Final Probe:** You probe the zombie again to get its new IP ID.
    
6. **Analysis:** If the IP ID has increased by 2, it _likely_ means the target port was open (the target's SYN/ACK caused one increment, and your final probe caused another). If the IP ID increased by 1, the port was closed or filtered. If it did not increase, the port was likely filtered.
    
The key is that you're not directly connecting to the target. The target's responses go to the zombie, and you infer the port state based on changes to the zombie's IP ID. Finding a truly idle zombie is crucial for accuracy.
### **V. Nmap Output and Options**

- **--reason:** Provides explanations for Nmap's conclusions about host and port states. Very useful for understanding _why_ Nmap thinks a port is open or closed.
    
- **-v (Verbose):** Increases the amount of information displayed.
    
- **-vv (Very Verbose):** Even more verbose output.
    
- **-d (Debug):** Shows debugging information, useful for troubleshooting Nmap itself.
    
- **-dd (More Debug):** Even more debugging detail.
    
- **--source-port PORT_NUM:** Lets you specify the source port for your scans. This can be useful for bypassing some firewalls that filter based on source port.