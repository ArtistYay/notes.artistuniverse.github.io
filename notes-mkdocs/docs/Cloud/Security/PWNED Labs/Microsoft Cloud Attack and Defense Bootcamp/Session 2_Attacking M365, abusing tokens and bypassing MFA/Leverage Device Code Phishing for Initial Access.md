Device code phishing is a dangerous technique, both in seeming legitimate to end users and in evading detection. In this lab you'll get hands on with real phishing, enumerate Azure resources, exploit an active Windows user and establish command and control (C2). This lab is good for both red and blue. Strap in!
## Learning outcomes  

- Device code phishing
- Azure enumeration using the Azure CLI and PowerShell
- Windows enumeration
- Windows lateral movement via binary hijacking
- Payload creation
- Controlling target systems using a C2
## Links

https://aadinternals.com/post/phishing/

https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-token-protection

https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-authentication-flows

https://learn.microsoft.com/en-us/troubleshoot/entra/entra-id/governance/verify-first-party-apps-sign-in#application-ids-of-commonly-used-microsoft-applications
## Attack Story and Command Explanation

This lab simulates a red team engagement against International Asset Management, targeting their cloud resources and executive accounts. The attack unfolds as follows:

**Phase 1: Reconnaissance and Phishing**

1. **DNS Enumeration**: The attack begins with enumerating DNS records using PowerShell or `dig` command. This reveals the mail server and website IP address.
    - `Resolve-DnsName`: PowerShell cmdlet to resolve DNS records of various types (A, AAAA, MX, TXT, NS, CNAME).
    - `dig`: Linux command-line utility for DNS queries.
2. **Microsoft 365 and Azure Verification**: The attacker confirms the use of Microsoft 365 and Entra ID by querying the `GetUserRealm.srf` endpoint. Further analysis of the website IP address using `ipinfo.io` and `azservicetags.azurewebsites.net` confirms the presence of Azure resources.
    - `Invoke-WebRequest`: PowerShell cmdlet to send web requests.
    - `curl`: Linux command-line tool for transferring data with URLs.
    - `jq`: Linux command-line JSON processor.
3. **Website Analysis**: The attacker discovers a contact form and client login portal on the company website. An attempt to log in with incorrect credentials reveals a support email address.
4. **Device Code Phishing**: The attacker crafts a phishing email containing a device code, exploiting the Entra ID device code authentication flow. The email prompts the recipient to approve the login request on a legitimate Microsoft login page.
    - `Invoke-RestMethod`: PowerShell cmdlet to send HTTP requests and handle responses.
    - `az login --use-device-code`: Azure CLI command to initiate device code authentication flow.

**Phase 2: Cloud Enumeration and Exploitation**

1. **Azure Resource Enumeration**: After successfully phishing the support account, the attacker uses the Azure CLI to enumerate Azure resources.
    - `az resource list`: Lists all resources within the subscription.
2. **Static Web App Analysis**: The attacker discovers an Azure Static Web App and retrieves its settings using the Azure CLI. This reveals sensitive information, including a database connection string with credentials.
    - `az staticwebapp show`: Displays information about a static web app.
    - `az staticwebapp appsettings list`: Lists the app settings for a static web app.
3. **Virtual Machine Analysis**: The attacker discovers an Azure Virtual Machine (VM) and retrieves its user data using a direct API call. The user data reveals a configuration script that enables the `remoteassist` local account on the VM.
    - `az vm show`: Displays information about a VM.
    - `Invoke-RestMethod`: PowerShell cmdlet used to send an API request to retrieve VM user data.
4. **VM Access and Lateral Movement**: The attacker uses Evil-WinRM to connect to the VM using the `remoteassist` account and the password found in the web app settings.
    - `evil-winrm`: A tool used for attacking Windows machines using WinRM.
5. **Binary Hijacking**: The attacker discovers a scheduled task that uses `pscp.exe` to transfer files. They replace this binary with a malicious version created using Shellter, injecting a Meterpreter payload.
    - `Shellter`: A tool used to inject shellcode into portable executables (PEs).
6. **C2 Communication**: The attacker sets up a Metasploit listener to handle the incoming Meterpreter session from the compromised VM.
    - `msfconsole`: Metasploit framework console.

**Phase 3: Post-Exploitation and Data Exfiltration**

1. **Meterpreter Session**: The attacker gains a Meterpreter session as the user `James_local` when the scheduled task executes the malicious `pscp.exe`.
2. **Privilege Escalation**: The attacker uses the Meterpreter session to navigate the file system and access sensitive data, including cloud credentials, achieving the objective of the engagement.

**Defense Recommendations**

The lab highlights several security weaknesses and provides recommendations for mitigating them:

- **Conditional Access Policies**: Enforce logins from managed devices and enable token protection to bind refresh tokens to specific devices.
- **Device Code Authentication Flow**: Consider disabling or restricting this authentication flow if not necessary.
- **Security Awareness Training**: Educate users about the dangers of device code phishing and suspicious login requests.
- **Anomaly Detection**: Monitor for anomalous user agents and interactive logins using the device code authentication protocol.

## Notes

- You can use `GetUserRealm.srf` endpoint to determine whether a domain name is managed (cloud-only) or a federated domain.
	- The **`GetUserRealm.srf` endpoint** is part of Microsoft's authentication system, commonly used in the background for services like Azure Active Directory (Azure AD) and Microsoft 365.
	 Here’s a simplified explanation:
	 **Purpose:** It determines how a specific user is set up to authenticate in Microsoft’s ecosystem. Essentially, it checks what kind of authentication is required for a user based on their email address or username.
	 **What it does:** When a service or application calls this endpoint with a user’s email or username, it responds with details about how the user should log in. For example:
		  Is the user using a cloud account (managed by Azure AD)?
		  Are they part of a federated system (using an external identity provider like AD FS)?Does the account use some other special method (like passwordless authentication)?
	 This endpoint helps Microsoft services decide how to route authentication requests or show the correct login experience for users.
	 In short, it’s like a "traffic director" for figuring out where and how a user’s login should be handled.
- [Device code phishing](https://aadinternals.com/post/phishing/) is a technique that takes advantage of a feature in Entra ID (formerly Azure AD) called **device code authentication flow**, which is designed for devices like TVs or consoles that don’t have a keyboard for typing in login credentials.
  Here’s how the flow works (legitimately):
	  1. On the device, the user is given a **code** and asked to go to a website (e.g., `microsoft.com/devicelogin`) on another device, like their phone or computer.
	  2. The user enters the code on the second device and logs in there.
	  3. Once logged in, the first device gets authenticated and can access resources.
	How phishing could exploit this:
		An attacker could:
			1. Trick a user into thinking they are completing a legitimate login process by showing them a fake prompt or asking them to enter a code on the legitimate Microsoft login page.
			2. Once the user enters the code and logs in, the attacker’s device (pretending to be the user’s) gets authenticated and gains access to the user’s resources.
  Why it works:
	  - The flow separates the device needing access from the one being used to log in, so users might not realize they’re authorizing an attacker’s session.
	  - The attacker leverages the **trust** users have in seeing the real Microsoft login page for entering the code.
  1. A user starts an app that supports device code flow on an device.
  2. The app connects to the Entra ID `/devicecode` endpoint and submits a `client_id` and `resource`.
  3. Entra ID returns a `device_code`, `user_code`, and `verification_url`.
  4. The device displays the `verification_url` ([https://microsoft.com/devicelogin](https://microsoft.com/devicelogin)) along with the `user_code` for the user.
  5. The user navigates to the `verification_url` in a web browser, enters the `user_code` as prompted, and logs in.
  6. The device continuously queries Entra ID and, once the login is verified as successful, it receives an `access_token` and a `refresh_token`.
- The client id is the Microsoft office ID. https://gist.github.com/dafthack/2c0bbcac72b10c1ee205d1dd2fed3fe7
	```$body=@{ "client_id" = "d3590ed6-52b3-4102-aeff-aad2292ab01c"` "resource" = "https://graph.microsoft.com" } $authResponse=(Invoke-RestMethod -UseBasicParsing -Method Post -Uri "https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0" -Body $body) $authResponse```


