Cybersecurity is an ongoing battle between security professionals ("white hat" hackers) and malicious actors ("black hat" hackers). As cyber threats become more sophisticated, organizations need specialized services to prepare for real-world attacks. Traditional security assessments like vulnerability assessments and penetration tests offer valuable insights but may not fully address all aspects of a real attack scenario.

**Vulnerability Assessments**

- **What was done:** Vulnerability assessments involve scanning a network's systems to identify as many vulnerabilities as possible.
    - Why? To provide a comprehensive overview of potential security weaknesses.
    - Why? To help the organization prioritize remediation efforts.
- **How it was done:** Automated tools are often used to scan hosts. In some cases, the attacker's machine may be allowlisted.
    - Why? To ensure the scanning process is not impeded by security solutions.
    - Why? To maximize the number of vulnerabilities identified.
- **Focus:** Individual hosts are scanned to identify security deficiencies.
- **Outcome:** A report detailing identified vulnerabilities, allowing the organization to take proactive measures to protect the network.
- **Example:** Scanning all hosts on a network for vulnerabilities without attempting to exploit them.

**Penetration Tests**

- **What was done:** Penetration tests go beyond vulnerability assessments by exploring the potential impact of vulnerabilities on the entire network.
    - Why? To understand how vulnerabilities can be chained together.
    - Why? To assess the overall risk to the organization.
- **How it was done:**
    - Attempting to exploit identified vulnerabilities.
        - Why? To confirm the exploitability of vulnerabilities.
        - Why? To test the effectiveness of compensatory controls.
    - Conducting post-exploitation tasks on compromised hosts.
        - Why? To determine the extent of potential damage.
        - Why? To identify opportunities for lateral movement.
- **Focus:** The network is viewed as an ecosystem, and the interactions between its components are considered.
- **Outcome:** A report detailing vulnerabilities, their potential impact, and how an attacker could exploit them to achieve specific goals.
- **Example:** Scanning hosts for vulnerabilities and then attempting to exploit them to demonstrate the potential impact.

**Limitations of Traditional Security Engagements**

- **What are they:** Traditional penetration tests may have limitations that prevent them from fully preparing an organization for a real-world attack.
- **Why?**
    - Penetration tests can be loud and easily detectable.
        - Why? Pentesters prioritize finding vulnerabilities quickly and efficiently.
        - Why? Time constraints often prevent pentesters from focusing on stealth.
    - Non-technical attack vectors (e.g., social engineering, physical intrusion) may be overlooked.
        - Why? The scope of penetration tests is often limited to technical vulnerabilities.
    - Security mechanisms may be relaxed during penetration tests.
        - Why? To ensure the penetration test can be completed within the allotted time.
        - Why? To avoid spending excessive time on bypassing security controls.
- **Advanced Persistent Threats (APTs):**
    - Highly skilled groups of attackers, often sponsored by nations or organized crime.
    - Target critical infrastructure, financial organizations, and government institutions.
    - Known for their ability to remain undetected on compromised networks for extended periods.
- **The Question:** Are organizations prepared to effectively respond to an APT attack?

**Red Team Engagements**

- **What are they:** Red team engagements simulate real-world attacks to assess an organization's ability to detect and respond to threats.
    - Why? To provide a more realistic approach to security testing.
    - Why? To focus on detection and response capabilities.
- **How are they different from penetration tests:** Red team engagements complement penetration tests by focusing on detection and response rather than just prevention.
- **Red Team Focus:** Emulating an adversary's Tactics, Techniques, and Procedures (TTPs) to measure the effectiveness of the "blue team" (defensive team).
- **Goals:** Red team engagements start by defining clear goals (e.g., compromising a critical host, stealing sensitive information).
- **Blue Team Awareness:** The blue team is typically unaware of the red team engagement to avoid biases in their analysis.
- **Red Team Actions:** The red team attempts to achieve its goals while remaining undetected and evading security mechanisms.
- **Host Interaction:** Red teams focus on finding a single path to their objective, rather than performing noisy scans of all hosts.
- **Outcome:** Red team engagements help organizations improve their detection and response capabilities by identifying weaknesses in their security controls.
- **Example:** A red team engagement with the goal of compromising an intranet server, focusing on stealth and evading detection.

**Key Concepts**

- **Crown Jewels/Flags:** The specific goals of a red team engagement.
- **Blue Team:** The defensive team responsible for protecting the organization's assets.
- **Tactics, Techniques, and Procedures (TTPs):** The methods used by attackers.
- **Detection and Response:** The focus of red team engagements.

**Red Team Engagement Improvements**

- Red team engagements improve on regular penetration tests by considering several attack surfaces:
    - **Technical Infrastructure:** Uncovering technical vulnerabilities with a focus on stealth and evasion.
    - **Social Engineering:** Targeting individuals through phishing, phone calls, or social media to obtain private information.
    - **Physical Intrusion:** Using techniques like lockpicking or exploiting weaknesses in access control systems to gain physical access to restricted areas.

**Types of Red Team Engagements**

- **Full Engagement:** Simulating an attacker's complete workflow, from initial compromise to achieving final objectives.
- **Assumed Breach:** Starting with the assumption that the attacker has already gained control over some assets.
- **Table-top Exercise:** A simulated discussion between red and blue teams to evaluate theoretical responses to certain threats.

**Red Team Engagement Personnel**

- **Teams/Cells:** Red team engagements typically involve three teams or cells:
    - **Red Cell:** The offensive component that simulates an attacker's actions.
    - **Blue Cell:** The defensive component, including the blue team, defenders, internal staff, and management.
    - **White Cell:** The referee between the red and blue cells, controlling the engagement environment, monitoring adherence to rules of engagement (ROE), and ensuring fairness.
- **Red Team Roles:**
    - **Red Team Lead:** Plans and organizes engagements, delegates tasks.
    - **Red Team Assistant Lead:** Assists the team lead, oversees operations, and may help with planning and documentation.
    - **Red Team Operator:** Executes delegated assignments and analyzes engagement plans.

**Adversary Emulation and Cyber Kill Chains**

- **Adversary Emulation:** A core function of red teams, which involves simulating the actions of real-world attackers.
- **Cyber Kill Chains:** Frameworks used to map adversary behaviors and break down their movements.
    - **Purpose:**
        - For blue teams: To map adversary behaviors and break down an adversary's movement.
        - For red teams: To map adversary TTPs to components of an engagement.
    - **Examples:**
        - Lockheed Martin Cyber Kill Chain
        - Unified Kill Chain
        - Varonis Cyber Kill Chain
        - Active Directory Attack Cycle
        - MITRE ATT&CK Framework
- **Lockheed Martin Cyber Kill Chain:** A standardized kill chain that focuses on external breaches.
    - **Components:**
        - **Reconnaissance:** Gathering information on the target (e.g., harvesting emails, OSINT).
        - **Weaponization:** Combining the objective with an exploit (e.g., exploit with backdoor, malicious document).
        - **Delivery:** How the weaponized function is delivered (e.g., email, web, USB).
        - **Exploitation:** Exploiting the target's system to execute code (e.g., MS17-010, Zero-Logon).
        - **Installation:** Installing malware or other tools (e.g., Mimikatz, Rubeus).
        - **Command & Control:** Controlling the compromised asset from a remote controller (e.g., Empire, Cobalt Strike).
        - **Actions on Objectives:** The ultimate goals, such as ransomware or data exfiltration (e.g., Conti, LockBit2.0).

**Conclusion**

Red team engagements provide a valuable way to assess an organization's ability to detect and respond to real-world cyber threats. By emulating adversary TTPs and considering various attack surfaces, red teams help organizations improve their security posture and better prepare for the evolving landscape of cybersecurity.