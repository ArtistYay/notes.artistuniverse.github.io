*Passwords aren't the only credentials! In this lab we use alternate forms of credential to get access and move laterally in Azure. Get ready to leverage service principals, web app managed identities and administrative units as we go from external, to the top of the tree!*

## Learning outcomes  

- Use certificate-based authentication to access service principal
- Leverage Website Contributor role to get command execution
- Move laterally from compromised web app using managed identity
- Enumerate Azure and Entra ID resources
- Leverage administrative unit permissions for lateral movement

**Scene 1: The Reconnaissance**

- **Attacker's Move:** The hacker starts by finding the company's Azure tenant ID using a public website (aadinternals.com). This is like finding the company's address before robbing a bank. They also try to guess employee emails and storage account names using tools like AzSubEnum and basicblobfinder.
    - **Attacker's Thinking:** Tenant ID is crucial for targeting Azure resources. Publicly available information and some educated guesses can reveal valuable targets.
    - **Defender's Misstep:** Failing to configure proper access controls on storage accounts. Storage accounts shouldn't be publicly accessible.
    - **Fix It:** Secure storage accounts with appropriate Network Security Groups (NSGs) to restrict access. Regularly scan for publicly exposed assets.

**Scene 2: The Jackpot**

- **Attacker's Move:** They stumble upon an unsecured storage account containing a treasure trove – a CSV file with application IDs and a PFX file with a certificate! This is like finding the bank's blueprints and a key to the vault.
    - **Attacker's Thinking:** "Bingo! Unprotected sensitive data is a goldmine. This certificate might give me access to something juicy."
    - **Defender's Misstep:** Storing sensitive credentials like certificates in an unsecured location. This is a major security no-no!
    - **Fix It:** Never store credentials in plain text or unprotected files. Use Azure Key Vault to securely store and manage certificates and keys.

**Scene 3: Impersonation**

- **Attacker's Move:** Using the certificate, the attacker impersonates a service principal (an application's identity in Azure) associated with the company's HR portal. They use commands like `openssl` (Linux) and `Import-PfxCertificate` (Windows) to import and utilize the certificate.
    - **Attacker's Thinking:** "Let's see what this service principal has access to. Maybe I can use it to move deeper into the network."
    - **Defender's Misstep:** Over-privileged service principal. The service principal had more access than it needed.
    - **Fix It:** Follow the principle of least privilege. Grant service principals only the minimal permissions necessary. Regularly audit and revoke unnecessary privileges.

**Scene 4: Web App Shenanigans**

- **Attacker's Move:** They discover an Azure web app connected to the HR portal. The attacker, using their impersonated identity, has the "Website Contributor" role, allowing access to sensitive configurations. They find the FTPS credentials for the web app.
    - **Attacker's Thinking:** "Website Contributor? Sounds powerful! Let's see if I can get code execution on this web app."
    - **Defender's Misstep:** Excessive privileges granted to the service principal on the web app.
    - **Fix It:** Review and restrict permissions on web apps. Use Azure RBAC (Role-Based Access Control) to fine-tune access and prevent privilege escalation.

**Scene 5: Backdoor Entry**

- **Attacker's Move:** They upload a webshell (a malicious script for remote control) to the web app using `curl`. This webshell allows them to execute commands on the web app server.
    - **Attacker's Thinking:** "Now I have a foothold in their web app! Time to explore further and escalate my privileges."
    - **Defender's Misstep:** Weak web application security. No measures in place to prevent malicious file uploads or detect webshells.
    - **Fix It:** Implement web application firewalls (WAFs) to filter malicious traffic. Regularly scan for webshells and malware on web servers.

**Scene 6: Identity Theft**

- **Attacker's Move:** The web app uses a managed identity to access other Azure resources. The attacker extracts the `IDENTITY_HEADER` and `IDENTITY_ENDPOINT` environment variables from the web app, allowing them to impersonate this managed identity as well.
    - **Attacker's Thinking:** "This managed identity might have access to even more sensitive resources! Let's ride this wave."
    - **Defender's Misstep:** Inadequate protection of managed identity credentials.
    - **Fix It:** Restrict access to environment variables containing sensitive information. Implement strong secrets management practices for all application components.

**Scene 7: The CEO's Downfall**

- **Attacker's Move:** Using the managed identity, the attacker gains access to Microsoft Graph API and discovers an administrative unit containing the CEO's account. They further find that their compromised identity has permissions to reset passwords within this administrative unit. They reset the CEO's password.
    - **Attacker's Thinking:** "Jackpot! The CEO's account is the crown jewel. With this, I can access almost anything."
    - **Defender's Misstep:** Overly permissive access controls on the administrative unit. The compromised identity should not have had password reset permissions for the CEO.
    - **Fix It:** Implement strong segregation of duties. Limit password reset permissions to authorized personnel only. Use Privileged Identity Management (PIM) for just-in-time privileged access.

**Scene 8: Game Over**

- **Attacker's Move:** The attacker logs in as the CEO using the newly reset password. They now have full control of the CEO's account and potentially the entire Azure environment.
    - **Attacker's Thinking:** "I'm in! Time to exfiltrate sensitive data, deploy ransomware, or cause some other mayhem."
    - **Defender's Misstep:** Lack of monitoring and alerting for suspicious activities, such as password resets for sensitive accounts or unusual access patterns.
    - **Fix It:** Implement robust monitoring and alerting systems, such as Azure Sentinel. Monitor for suspicious logins, unusual API calls, and any activity indicative of an attacker.

**Alternative Attacker Tools & Techniques:**

- **Enumeration:** Instead of AzSubEnum, the attacker could have used tools like `Sublist3r` or `Amass` to enumerate subdomains. These tools might provide a broader range of potential targets but could also generate more noise and take longer.
- **Webshell:** The attacker could have used a different type of webshell, such as an ASPX webshell for a Windows-based web app, or a more sophisticated webshell with advanced features like evasion techniques.
- **Lateral Movement:** The attacker could have tried to exploit vulnerabilities in other Azure services or leverage techniques like pass-the-hash or pass-the-ticket to move laterally within the network.

**Defender's Perspective:** This attack chain highlights critical security gaps in Mega Big Tech's cloud environment. Implementing a defense-in-depth strategy, following least privilege principles, and establishing robust monitoring and incident response capabilities are essential to prevent and mitigate such attacks.
## Notes 

- KQL query that detects managed identities retrieving a Web App publish profile.
	` // Display Activity log Administrative events // Displays Activity log for Administrative category. AzureActivity | where CategoryValue == "Administrative" and OperationNameValue contains "MICROSOFT.WEB/SITES/PUBLISHXML/ACTION" | order by TimeGenerated desc`

## Links

[Russia-based group hacked emails of Microsoft’s senior leadership](https://www.csoonline.com/article/1296269/russia-based-group-hacked-emails-of-microsofts-senior-leadership.html)

[Administrative units in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/administrative-units)