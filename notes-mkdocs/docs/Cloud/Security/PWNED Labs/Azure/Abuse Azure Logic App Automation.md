## Notes

### **Step 1: Open-Source Intelligence (OSINT)**

- **Attacker’s Perspective:**
    
    - **Action:** Found sensitive information (e.g., DevTeamVM IP, Azure Subscription ID) in a LinkedIn post screenshot.
    - **Rationale:** Public social media posts often inadvertently leak sensitive organizational data.
    - **Commands:**
        - Research DNS records for company infrastructure:
            
            ```bash
            dig megabigtech.com +noall +answer ANY
            ```
            
        - Extract email formats and infrastructure insights.
- **Defender’s Perspective:**
    
    - **Vulnerability:** Employees sharing sensitive screenshots or posts online.
    - **Prevention:**
        - Conduct regular security awareness training focusing on social media practices.
        - Implement Data Loss Prevention (DLP) solutions to monitor and block sensitive data exposure.
        - Use image-scanning tools to detect sensitive information in public posts.
    - **Remediation:**
        - Take down the post.
        - Conduct a risk assessment on exposed information.

---

### **Step 2: Email Enumeration**

- **Attacker’s Perspective:**
    
    - **Action:** Verified email existence using enumeration tools.
    - **Tool:** [`o365enum`](https://github.com/gremwell/o365enum).
    - **Command:**
        
        ```bash
        python3 o365enum.py -u email.txt -m office.com
        ```
        
    - **Rationale:** To confirm a valid attack target by enumerating Microsoft 365 email accounts.
- **Defender’s Perspective:**
    
    - **Vulnerability:** Misconfigured Microsoft 365 responses revealing account existence.
    - **Prevention:**
        - Enable Azure AD Smart Lockout to block repeated enumeration attempts.
        - Use Conditional Access to limit access from suspicious IP ranges.
    - **Remediation:**
        - Review and enforce email address verification throttling.
        - Monitor login activity for abnormal patterns.

---

### **Step 3: Password Spray**

- **Attacker’s Perspective:**
    - **Action:** Used likely passwords (e.g., `superRyan!`) derived from the OSINT findings.
    - **Tool:** [`o365spray`](https://github.com/0xZDH/o365spray).
    - **Command:**
        
        ```bash
        python3 o365spray.py --username ryan.lin@megabigtech.com --passfile passwords.txt --domain megabigtech.com --lockout 
        ```
## Links

https://learn.microsoft.com/en-us/connectors/office365users/#get-manager-(v2)

[Illogical Apps – Exploring and Exploiting Azure Logic Apps](https://www.netspi.com/blog/technical-blog/cloud-pentesting/illogical-apps-exploring-exploiting-azure-logic-apps/)

[Work with Logic Apps or Power Automate](https://learn.microsoft.com/en-us/dynamics365/fraud-protection/extensibility-with-power-automate)