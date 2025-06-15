*In lab we'll explore how secrets can be leveraged to move laterally and vertically in an Azure environment. You'll get hands-on experience with ROADrecon and interact with virtual machines and automation accounts.*

## Learning outcomes 

- Reveal password that is masked using the iOS Markup tool
- Azure situational awareness using the CLI and ROADrecon
- Identify and exploit Azure attack paths
- Abuse Entra ID to gain privileges
- Automation account enumeration and secret exfiltration

## Attack Story Breakdown

1. **Reconnaissance**:
    
    - The attacker identifies a target employee (Matteus Lundgren) through LinkedIn.
    - Observing an image in Matteus’s post, they suspect the obfuscation of sensitive information on a Post-It note using iOS Markup.
    - Using image manipulation techniques (e.g., GIMP), the attacker reveals the password `SUMMERDAZE1!`.
    
    **Takeaway**:
    
    - Publicly available information on social media is often exploited by attackers during reconnaissance.
    - Employees need training on avoiding unintentional data leaks and on using reliable redaction tools.
2. **Initial Access**:
    
    - The attacker guesses Matteus’s corporate email (`matteus@megabigtech.com`) using typical email patterns found during recon.
    - They authenticate to Azure using the revealed password.
    
    **Takeaway**:
    
    - Password reuse is a significant vulnerability.
    - Multi-Factor Authentication (MFA) would have stopped the attacker from logging in even with valid credentials.
3. **Situational Awareness**:
    
    - After gaining access, the attacker uses Azure CLI commands like `az resource list` to map the environment.
    - They identify a virtual machine (`AUTOMAT01`) in the `mbt-rg-5` resource group, its OS details, and the user `automation` with SSH access.
    
    **Takeaway**:
    
    - Principle of least privilege is essential. Restrict what resources users can view or access based on their job role.
4. **Lateral Movement**:
    
    - Using ROADrecon, the attacker explores Entra ID (formerly Azure AD) to find their current user’s permissions and roles.
    - They identify ownership of a privileged group (`DEVICE-ADMINS`) and escalate privileges by adding themselves to this group.
    
    **Takeaway**:
    
    - Privileged group ownership should be closely monitored, and risky group operations (like adding members) should trigger alerts.
    - Conditional Access policies can further restrict what privileged actions are allowed.
5. **Privilege Escalation and Sensitive Data Access**:
    
    - After refreshing their session, the attacker accesses the `Devices-new` Key Vault, which contains sensitive secrets.
    - They extract a secret (`AUTOMAT01`) to potentially compromise the VM.
    
    **Takeaway**:
    
    - Secrets and sensitive data in Azure Key Vault should use strict access control and audit logging.
    - Regularly rotate secrets and enforce RBAC policies for least privilege.

## Notes

"pip install roadrecon error: externally-managed-environment × This environment is externally managed ╰─> To install Python packages system-wide, try apt install python3-xyz, where xyz is the package you are trying to install. If you wish to install a non-Kali-packaged Python package, create a virtual environment using python3 -m venv path/to/venv. Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make sure you have pypy3-venv installed. If you wish to install a non-Kali-packaged Python application, it may be easiest to use pipx install xyz, which will manage a virtual environment for you. Make sure you have pipx installed. For more information, refer to the following: * https://www.kali.org/docs/general-use/python3-external-packages/ * /usr/share/doc/python3.12/README.venv"

This error occurs because your environment is configured as "externally managed," meaning direct system-wide package installations with `pip` are restricted. This is common in distributions like Kali Linux to prevent conflicts with system-managed packages.

Here’s how you can proceed:

**Use a Virtual Environment**

This is the recommended approach for installing Python packages without affecting the system Python installation.

Create a virtual environment: python3 -m venv roadrecon-venv  

Activate the virtual environment: source roadrecon-venv/bin/activate  

Install roadrecon within the virtual environment: pip install roadrecon

Once installed, you can use `roadrecon` within the virtual environment. To exit the virtual environment, run: `deactivate`

## Links
[Security best practices in Azure Automation](https://learn.microsoft.com/en-us/azure/automation/automation-security-guidelines)
