This lab highlights how securely configured Azure Web App resources can be undone by a single flaw in deployed code! Get hands-on with Burp Suite to enumerate web resources and exploit a path traversal vulnerability.
## Learning outcomes  

- Enumerate Azure Web Apps using the Az PowerShell module
- Identify and exploit a simple path traversal vulnerability
- Use Burp Suite to enumerate server resources
## Notes

### **Step-by-Step Cloud Penetration Testing Narrative**

---

#### **Step 1: Establish Initial Access**

**Attack:**  
The attacker uses stolen credentials from a phishing attack to establish an authenticated Azure session with the `Connect-AzAccount` command.

**Command:**

```powershell
Connect-AzAccount
```

**Attacker's Perspective:**

- **Why:** Compromising credentials is the first step to establishing access. Azure sessions can reveal information about the resources accessible to the compromised account.
- **Alternative Approaches/Tools:** Other tools like `Azure CLI` or REST API could have been used. Azure PowerShell was chosen for its user-friendly integration and comprehensive resource enumeration.

**Defense:**

- **Prevention:** Implement multi-factor authentication (MFA) to mitigate credential compromise. Monitor and flag suspicious login attempts.
- **Mitigation:** Use conditional access policies to restrict access based on location or device compliance. Monitor sign-ins with Azure AD logs for anomalous behavior.

---

#### **Step 2: Resource Enumeration**

**Attack:**  
The attacker enumerates Azure resources using `Get-AzResource`.

**Command:**

```powershell
Get-AzResource
```

**Attacker's Perspective:**

- **Why:** To identify valuable resources the user has access to. This is critical for targeting applications or services with vulnerabilities.
- **Alternative Tools:** Azure CLI (`az resource list`) offers similar capabilities but lacks PowerShell's scripting flexibility.

**Defense:**

- **Prevention:** Apply the principle of least privilege (PoLP) to ensure user accounts only have access to necessary resources.
- **Mitigation:** Enable resource access logging and review access permissions regularly.

---

#### **Step 3: Path Traversal Discovery**

**Attack:**  
The attacker exploits a path traversal vulnerability by manipulating the `status` query parameter in the Azure Web App URL.

**Command:**

```plaintext
https://megabigtech-dev.azurewebsites.net/status.aspx?status=..\status.aspx.cs
```

**Attacker's Perspective:**

- **Why:** Path traversal can expose sensitive files, such as source code, credentials, or configuration data.
- **Alternative Approaches:** Using automated tools like Burp Suite or OWASP ZAP to identify vulnerabilities with fuzzing techniques. Manual attempts are precise but time-intensive.

**Defense:**

- **Prevention:** Validate and sanitize user input to prevent directory traversal attacks. Disallow special characters like `../` in query parameters.
- **Mitigation:** Implement a web application firewall (WAF) to block malicious requests.

---

#### **Step 4: Resource Enumeration with Burp Suite**

**Attack:**  
The attacker uses Burp Suite's Intruder tool to enumerate directories and files hosted on the Azure Web App.

**Steps in Burp Suite:**

1. Capture an authenticated request.
2. Send the request to Intruder.
3. Use a directory wordlist to fuzz potential paths.
4. Analyze the responses to identify valid resources.

**Attacker's Perspective:**

- **Why:** Automated enumeration quickly reveals hidden resources like `admin` and `login.aspx`.
- **Alternative Tools:** Tools like Gobuster or Dirbuster offer faster enumeration but may require specific configurations.

**Defense:**

- **Prevention:** Use strict access controls on sensitive directories. Avoid exposing unnecessary resources publicly.
- **Mitigation:** Periodically scan the application with tools like Burp Suite to identify and remediate directory enumeration vulnerabilities.

---

#### **Step 5: Exploiting the Admin Panel**

**Attack:**  
The attacker discovers credentials in the `login.aspx.cs` file and uses them to access the admin panel.

**Command:**

```plaintext
https://megabigtech-dev.azurewebsites.net/admin/login.aspx
```

**Attacker's Perspective:**

- **Why:** Admin panels often have elevated privileges, allowing full control over the application.
- **Alternative Approaches:** Brute-forcing login credentials might work but could trigger account lockout or monitoring alerts.

**Defense:**

- **Prevention:** Do not hardcode sensitive credentials in code files. Use Azure Key Vault to securely store credentials.
- **Mitigation:** Implement rate-limiting and account lockout mechanisms to prevent brute force attacks. Enable logging and alerts for admin panel access.

---

#### **Remediation Advice for Each Vulnerability**

1. **Phishing Defense:**
    
    - Train users to recognize phishing attempts.
    - Use email filtering solutions to block phishing emails.
2. **Excessive Permissions:**
    
    - Conduct regular access reviews to minimize excessive permissions.
    - Use Azure Role-Based Access Control (RBAC) to manage access.
3. **Path Traversal:**
    
    - Sanitize inputs and validate file paths strictly.
    - Limit file access to specific directories using server configurations.
4. **Sensitive Data in Source Files:**
    
    - Use secure coding practices and secret management solutions like Azure Key Vault.
    - Conduct regular code reviews and static analysis scans.
5. **Directory Enumeration:**
    
    - Configure the server to return generic error messages.
    - Block access to directories through `.htaccess` or equivalent server settings.

---

#### **Alternative Tools for the Attack**

|**Tool/Command**|**Advantages**|**Disadvantages**|
|---|---|---|
|**Azure CLI**|Lightweight and cross-platform.|Lacks some advanced PowerShell features.|
|**OWASP ZAP**|Free and open-source.|Requires manual setup and configuration.|
|**Nmap with NSE Scripts**|Useful for scanning Azure services.|Limited to network-level enumeration.|

---

This walkthrough demonstrates how a simple misconfiguration and weak code practices can lead to severe breaches. Regular security assessments and implementing best practices are essential for protecting cloud environments.
## Links

https://portswigger.net/burp/documentation/desktop/external-browser-config

https://hackerone.com/reports/217344