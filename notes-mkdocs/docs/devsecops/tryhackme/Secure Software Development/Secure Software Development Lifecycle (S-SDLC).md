### Introduction to S-SDLC

- **Goal:** Integrate security at _every_ stage of the Software Development Lifecycle (SDLC). This is a proactive approach, rather than reactive.

![screenshot](../../../images/3d1e3379a1e3ccc46f3c7471095cbfae.png)

### Implementing S-SDLC - The Prep Work

- **Understand Your Security Posture:** Before implementing S-SDLC, you need a clear picture of your current security state.
- **Gap Analysis:** Identify the differences between your current security practices and desired state. What's missing?
- **Software Security Initiatives (SSI):**
    - Establish realistic and achievable security goals.
    - Define metrics to measure success.
    - _Examples:_ Secure Coding Standard, data handling playbooks.
    - Track progress using project management tools.
### Risk Assessment - Understanding the Threat

- **Risk:** The likelihood of a vulnerability being exploited.
- **Types of Risk Assessment:**
    - **Qualitative:**
        - Formula: Risk = Severity x Likelihood.
        - Classification: Low, Medium, High.
        - _Benefit:_ Quick and easy to understand.
    - **Quantitative:**
        - Uses numerical values to calculate risk.
        - _Example:_ Annual Loss Expectancy (ALE) = Potential Loss x Number of Assets x Annual Rate of Occurrence (ARO).
        - _Benefit:_ More precise, allows for cost-benefit analysis of security controls.
        - _Example:_ If a data breach could cost $20,000 per customer, and you have 100 customers, and the ARO is 0.001, then ALE = $2,000. If a security control costs less than $2,000 annually, it's worth implementing.
        - _Business Criticality:_* Assign points to services based on their importance to the business (e.g., authentication = 5 points).
		    ![screenshot](../../../images/e5fb607dfd764c3e162da1783dd58e02.png)
    
### Threat Modeling - Identifying Vulnerabilities

- **Purpose:** Systematically identify potential threats and vulnerabilities.
- **Methods:**
    - **DREAD:** Damage, Reproducibility, Exploitability, Affected Users, Discoverability. A risk rating system.
    - **STRIDE:** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. Focuses on the CIA triad (Confidentiality, Integrity, Availability).
    - **PASTA:** Process for Attack Simulation and Threat Analysis. Aligns technical requirements with business objectives.
### Secure Coding - Building Security In

- **Goal:** Prevent vulnerabilities from being introduced in the first place.
- **Vulnerability Mitigation:** Can be done manually or automatically.
- **Security Testing Tools:**
    - **SAST (Static Application Security Testing):** Analyzes source code _before_ compilation. Detects potential vulnerabilities. Includes SCA (Software Composition Analysis) to check open-source components.
    - **DAST (Dynamic Application Security Testing):** Scans _running_ applications for vulnerabilities.
    - **IAST (Interactive Application Security Testing):** Real-time testing in a staging environment. Identifies the specific line of code causing issues. Occurs post-build, unlike SAST.
    - **RASP (Runtime Application Self Protection):** Deployed on the application server. Monitors traffic and blocks malicious requests in real-time. Protects against various attacks without relying on specific vulnerability signatures.
### Security Assessment - Finding Weaknesses

- **Goal:** Evaluate the security of a system, software, or web application.
- **Methods:**
    - Vulnerability Assessment: Identifies potential weaknesses.
    - Penetration Testing: Simulates real-world attacks to uncover vulnerabilities.
- **Timing:** Often performed during the Operations & Maintenance phase.
### S-SDLC Methodologies - Frameworks for Implementation

- **Microsoft's Security Development Lifecycle (SDL):** A prescriptive process with defined stages and activities.

![screenshot](../../../images/Pasted image 20241009155434.png)

- **OWASP Secure Software Development Life Cycle Project (S-SDLC):** Provides guidance and resources for implementing S-SDLC. OWASP SAMM (Software Assurance Maturity Model) can be used to assess and improve an organization's security posture. [OWASP Secure Software Development Life Cycle Project (S-SDLC)](https://owasp.org/www-project-samm/)

![screenshot](../../../images/Pasted image 20241009155500.png)