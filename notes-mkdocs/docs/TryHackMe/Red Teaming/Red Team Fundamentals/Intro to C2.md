A C2 framework is a system used by threat actors (and security professionals in red team exercises) to maintain control over compromised devices. At its core, a C2 framework enables:

- **Centralized management** of multiple compromised hosts.
- **Advanced post-exploitation capabilities** beyond simple reverse shells.
- **Flexible payload delivery and obfuscation techniques** to evade detection.
#### Why is this important?

- A simple Netcat listener can handle reverse shells, but it lacks the ability to manage multiple sessions efficiently.
- C2 frameworks provide structured communication between compromised hosts and the attacker.
- Understanding C2 frameworks helps in detecting and mitigating advanced persistent threats (APTs).
# Command and Control Framework Structure

## C2 Server

- Acts as the command hub, waiting for infected hosts (agents) to connect.
- Listens for incoming beacons and executes commands remotely.
### Why does the C2 server need to exist?

- Attackers need a persistent way to control compromised machines.
- Without a central server, managing multiple compromised systems would be chaotic.
## Agents / Payloads

- The software running on the compromised host that communicates with the C2 server.
- Can execute commands, upload/download files, and perform other malicious actions.
- Highly configurable to adjust beaconing behavior (e.g., how often it calls back to the server).
## Listeners

- Processes running on the C2 server that wait for incoming connections from agents.
- Support different protocols like DNS, HTTP, HTTPS.
## Beacons

- The process of an agent "checking in" with the C2 server at set intervals.
## Sleep Timers

- Attackers introduce delays between agent callouts to mimic normal network traffic.
- Example: An agent beaconing every 5 seconds is highly detectable.
## Jitter

- Introduces randomness to beaconing intervals to evade detection.
- Example: Instead of always calling back every 60 seconds, an agent calls back within a randomized range (e.g., 45–75 seconds).

```python
import random

sleep = 60  # Base sleep time
jitter = random.randint(-30, 30)  # Add randomness
sleep = sleep + jitter
```

1. **Why do C2 agents beacon?** To maintain persistent communication with the C2 server.
2. **Why is persistence important?** Attackers need long-term access for data exfiltration or lateral movement.
3. **Why can’t they maintain a permanent connection?** Continuous traffic is easily detected.
4. **Why is detection a risk?** Security tools analyze network traffic patterns to flag irregular activity.
5. **Why do attackers use beaconing with jitter?** To blend in with normal user traffic and evade detection.
# Payloads

## Stageless Payloads

- Contain the full agent in a single package.
- Immediately begin beaconing after execution.
	![[Pasted image 20250331170824.png]]
## Staged Payloads

- Download additional payloads from the C2 server after execution.
- Smaller initial footprint reduces detection risk.
	![[Pasted image 20250331170759.png]]
### Why use a staged approach?

- **Detection avoidance**: A small, benign-looking file is less likely to be flagged.
- **Flexibility**: The second stage can be customized or updated dynamically.
#### Payload Formats

- Attackers use various formats to bypass security:
    - **PowerShell scripts** (easier execution within Windows environments).
    - **HTA files** (often used in phishing attacks).
    - **JScript/VBScript** (leverages built-in Windows functionality).
    - **Office macros** (popular method for social engineering).

1. **Why not just use a standard executable?** Security tools scan and block common executable files.
2. **Why do attackers favor scripting languages?** They are interpreted in memory, reducing file-based detection.
3. **Why does in-memory execution matter?** It avoids creating disk artifacts that security tools can scan.
4. **Why are Office macros still used?** Many organizations still allow macro-enabled documents.
5. **Why do companies allow macros?** They are needed for legitimate business functions.
# Modules in C2 Frameworks

## Post-Exploitation Modules

- Extend C2 capabilities beyond initial access.
- Example: Running _SharpHound.ps1_ to map Active Directory relationships.
## Pivoting Modules

- Enable access to restricted networks by tunneling through compromised hosts.
- Example: Using an SMB Beacon to route traffic through an infected machine.
    ![[Pasted image 20250331170501.png]]
#### Why does pivoting matter?

- Many networks segment sensitive assets.
- Pivoting allows attackers to navigate these segments stealthily.
# Hiding C2 Infrastructure

## Domain Fronting

- Routes traffic through trusted cloud services (e.g., Cloudflare) to obscure its true destination.
    ![[Pasted image 20250331170609.png]]
1. The victim connects to a legitimate cloud service (e.g., Cloudflare).
2. Cloudflare proxies the request to the attacker's hidden C2 server.
3. The C2 server responds, appearing as normal traffic from a trusted provider.
## C2 Profiles

- Attackers customize HTTP requests to evade detection.
- Example: Using special headers or request patterns only understood by the C2 server.
	![[Pasted image 20250331170649.png]]
# Links

https://blog.zsec.uk/cobalt-strike-profiles/

https://www.recordedfuture.com/cobalt-strike-servers/

https://2017.zeronights.org/wp-content/uploads/materials/ZN17_SintsovAndreyanov_MeterpreterReverseDNS.pdf


