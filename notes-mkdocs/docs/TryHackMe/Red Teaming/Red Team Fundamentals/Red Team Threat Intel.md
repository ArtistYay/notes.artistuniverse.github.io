
Threat Intelligence (TI) provides defenders with insight into adversary behaviors, tactics, techniques, and procedures (TTPs). However, the **red team** can also leverage CTI to emulate adversaries more accurately and assess blue team defenses.
# Key Takeaways:

- CTI is not just a defensive tool—it enables **adversary emulation**, helping red teams refine attack scenarios and improve realism.
- TTPs provide a deeper understanding of how an adversary **operates**, moving beyond simple Indicators of Compromise (IOCs).
- CTI platforms such as **MITRE ATT&CK, TIBER-EU, and OST Map** aid in mapping TTPs and planning engagements.
### Why is this important?  

1. Why use CTI in red teaming? → To simulate real-world attacks based on known adversary behaviors.
2. Why simulate real-world attacks? → To test and improve defensive capabilities effectively.
3. Why improve defenses? → To reduce risk and prevent breaches.
4. Why prevent breaches? → To protect sensitive data and business operations.
5. Why is this critical? → A more **resilient security posture** protects organizations from real adversaries.

---
CTI is actionable intelligence that can be **consumed** in various ways, such as tracking adversary **IOCs** (e.g., domains, IPs, malware hashes) and **TTPs** (e.g., attack methodologies).
# Methods of CTI Consumption:

- **ISACs (Information Sharing and Analysis Centers):** Shared intelligence repositories.
- **Threat Intelligence Platforms:** Automated aggregation and categorization of threat data.
- **Public Frameworks (e.g., MITRE ATT&CK):** Organizing adversary TTPs into structured models.
## Why focus on TTPs instead of just IOCs?

- **IOCs change frequently** (e.g., an IP address can be abandoned).
- **TTPs remain consistent**—adversaries tend to follow similar operational patterns.

 **Reflection:**  
 A red team can assess a blue team’s effectiveness by **determining how well they leverage CTI** for detections. If a blue team only focuses on IOCs, they may **miss detecting novel threats** using the same TTPs.

---
Once an adversary is selected, their TTPs should be mapped to a **cyber kill chain** to model attack progression.
# Steps for TTP Mapping:

1. **Select an adversary** based on industry, attack vectors, or geopolitical motivation.
2. **Use MITRE ATT&CK** to collect their TTPs.
3. **Map these TTPs** to the Lockheed Martin Cyber Kill Chain (or an equivalent model).

 **Example: APT 39 (Iranian Espionage Group) Mapped to the Kill Chain**

|**Kill Chain Phase**|**Mapped TTPs (MITRE ATT&CK)**|
|---|---|
|**Reconnaissance**|No identified TTPs, use internal methodology|
|**Weaponization**|PowerShell, Python, VBA scripting|
|**Delivery**|Spearphishing, exploiting public-facing apps|
|**Exploitation**|Registry modifications, keylogging, credential dumping|
|**Installation**|Ingress tool transfer, proxy usage|
|**C2 (Command & Control)**|Web protocols (HTTP/HTTPS), DNS tunneling|
|**Actions on Objectives**|Exfiltration over C2|

 **Why is TTP mapping crucial?**

- It enables **structured attack planning** rather than ad-hoc engagements.
- It aligns tactics with real-world **adversary behaviors** for realistic testing.
- It ensures **consistency in emulation**, providing meaningful results in assessments.

---
During execution, the red team **modifies behavior and tooling** based on collected intelligence.
# Practical Use Cases:

- **Malleable C2 Profiles:** Adjusting C2 traffic (e.g., using collected Host Headers, URIs, etc.) to mimic adversary behavior.
- **Emulating Malware Behaviors:** Modifying dropper characteristics (e.g., syscalls, API calls) to avoid simple detection.
- **User-Agent and Protocol Manipulation:** Ensuring network traffic resembles actual adversaries.

 **Example: C2 Traffic Manipulation**

- A red team may modify a Cobalt Strike C2 profile using known **adversary indicators** (e.g., domain fronting, custom headers) to evade detection.
- This forces defenders to **improve detection mechanisms**, ensuring their blue team isn't just relying on basic IOC blocklists.

 **Why does this matter?**

- If a defender only detects standard Cobalt Strike traffic, but **not modified profiles**, they have a **glaring blind spot** in their detection capabilities.
- Red teams must adapt adversary behaviors dynamically to provide **real value** to security programs.

---
A **threat-intel-driven campaign** takes all of these components and integrates them into a **structured** engagement plan.
# Campaign Planning Steps:

1. **Identify the Framework & Kill Chain** (e.g., MITRE ATT&CK, Lockheed Martin Cyber Kill Chain).
2. **Select the Target Adversary** (APT group aligned with industry threats).
3. **Collect & Analyze TTPs and IOCs** (using MITRE ATT&CK, TIBER-EU, etc.).
4. **Map Intelligence to a Framework** (assign TTPs to corresponding kill chain phases).
5. **Develop Engagement Documentation** (Rules of Engagement, Attack Plans).
6. **Prepare Execution Resources** (custom malware, C2 modifications, infrastructure setup).

 **Challenges in Campaign Planning:**

- **Mapping different frameworks** (e.g., aligning MITRE ATT&CK with Lockheed Martin Cyber Kill Chain).
- **Ensuring accurate adversary emulation** without unnecessary complexity.
- **Balancing realism and operational constraints** (e.g., client rules, ethical concerns).

 **Final Reflection:**

- **Threat intelligence is NOT just data collection—it’s a decision-making tool.**
- **Adversary emulation forces defenders to improve beyond signature-based detection.**
- **Red team success is measured by how effectively they challenge and improve blue team capabilities.**