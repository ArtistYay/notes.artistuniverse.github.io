
This lab showcases how threat actors can achieve their objectives in Azure by performing the "credential shuffle", and working their way through the Azure kill chain. The focus of this lab is using tools as an admin would, as well as introducing offensive tooling.  
  
## Learning outcomes  

- Entra ID enumeration
- Gain an understanding of the Azure kill chain
- Leverage service principal control to move laterally
- Azure Windows Virtual Machine post-exploitation
- Enumeration of storage accounts and containers

## Notes

This walkthrough focuses on a structured red team engagement targeting an Azure environment. It highlights various attack stages, associated commands, and mitigation strategies. Here's the attack story step-by-step with detailed insights and remediation recommendations.

---

### **Step 1: Initial Access**

**Narrative:** The attacker gains access to credentials (e.g., `dbuser`) from a connection string exposed in an Azure Web App.

**Command:**

```powershell
$passwd = ConvertTo-SecureString "V%#J3c5jceryjcE" -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential("dbuser@megabigtech.com",$passwd)
Connect-AzAccount -Credential $creds
```

#### Attacker's Perspective:

- **Why this approach?** Connection strings often contain embedded credentials that attackers can leverage.
- **Advantages:** Immediate access to Azure Resource Manager using the exposed credentials.
- **Alternative Tools:**
    - **Azure CLI:** Can also authenticate with `az login --service-principal` if the attacker obtains a service principal ID and secret.

#### Defender's Perspective:

- **How could this be prevented?** Avoid hardcoding sensitive credentials in connection strings.
- **Remediation:**
    - Use **Managed Identity** to eliminate the need for embedded credentials.
    - Regularly scan for exposed secrets using tools like **Microsoft Defender for DevOps**.

---

### **Step 2: Entra ID Enumeration**

**Narrative:** The attacker enumerates the Azure Active Directory (AAD) to find privileged accounts or groups.

**Command:**

```powershell
Install-Module -Name Microsoft.Graph
Connect-MgGraph -Credential $creds
Get-MgUserMemberOf -UserId dbuser@megabigtech.com
```

#### Attacker's Perspective:

- **Why this approach?** Identifies potential roles or group memberships for privilege escalation.
- **Advantages:** Explores role assignments and administrative units efficiently.
- **Alternative Tools:**
    - **BloodHound-Azure:** Graph-based visualization of AAD roles and permissions.
    - **AzureHound:** Enumerates Azure and AAD relationships.

#### Defender's Perspective:

- **How could this be prevented?** Limit role assignments and adopt the principle of least privilege.
- **Remediation:**
    - Implement **Conditional Access Policies** to enforce MFA and limit access based on user risk.
    - Use **AAD Privileged Identity Management (PIM)** to require just-in-time elevation for sensitive roles.

---

### **Step 3: Privilege Escalation**

**Narrative:** The attacker discovers the ability to reset the password of another user (e.g., `Daiki Hiroko`).

**Command:**

```powershell
$params = @{
    passwordProfile = @{
        forceChangePasswordNextSignIn = $false
        forceChangePasswordNextSignInWithMfa = $false
        password = "Password12345!!"
    }
}
Update-MgUser -UserId 'Daiki.Hiroko@megabigtech.com' -BodyParameter $params
```

#### Attacker's Perspective:

- **Why this approach?** The `Authentication Administrator` role allowed resetting passwords.
- **Advantages:** Directly establishes control over another user account.
- **Alternative Tools:** Manual API calls via **Microsoft Graph API Explorer**.

#### Defender's Perspective:

- **How could this be prevented?** Limit the scope of administrative roles.
- **Remediation:**
    - Review and restrict role assignments in **AAD Role-Based Access Control (RBAC)**.
    - Monitor role changes using **Azure AD Logs** and **Microsoft Sentinel Analytics Rules**.

---

### **Step 4: Service Principal Misuse**

**Narrative:** The attacker adds secrets to a service principal they control.

**Command:**

```powershell
$newPassword = Add-MgApplicationPassword -ApplicationId $appId -PasswordCredential $passwordCred
```

#### Attacker's Perspective:

- **Why this approach?** Service principals bypass user-focused controls like MFA.
- **Advantages:** Persistent access with minimal detection risk.
- **Alternative Tools:**
    - **AADInternals:** Automates service principal enumeration and exploitation.

#### Defender's Perspective:

- **How could this be prevented?** Enforce strict monitoring and lifecycle management of service principals.
- **Remediation:**
    - Audit service principals and their secrets using **Azure AD Access Reviews**.
    - Rotate secrets periodically and remove unused service principals.

---

### **Step 5: Storage Account Enumeration**

**Narrative:** The attacker uses the `Storage Blob Data Reader` role to enumerate and download sensitive data.

**Command:**

```powershell
$context = New-AzStorageContext -StorageAccountName storageqaenv
Get-AzStorageBlob -Container "general-purpose" -Context $context
Get-AzStorageBlobContent -Container "general-purpose" -Blob "Dev-cred.txt" -Context $context
```

#### Attacker's Perspective:

- **Why this approach?** The role allows listing and downloading blobs.
- **Advantages:** Targets potentially sensitive configuration files.
- **Alternative Tools:**
    - **AZCopy:** For efficient blob enumeration and download.

#### Defender's Perspective:

- **How could this be prevented?** Apply granular access controls to storage containers.
- **Remediation:**
    - Enable **Azure Storage Firewalls** to restrict access to trusted IP ranges.
    - Use **Azure Defender for Storage** to detect anomalous access patterns.

---

### **Step 6: Lateral Movement**

**Narrative:** The attacker establishes a PowerShell Remoting session on an Azure VM using the compromised credentials.

**Command:**

```powershell
$vm = New-PSSession -ComputerName 172.191.90.57 -Credential $cred
Enter-PSSession -Session $vm
```

#### Attacker's Perspective:

- **Why this approach?** Targets a VM for potential privilege escalation or persistence.
- **Advantages:** Exploits trust relationships in hybrid environments.
- **Alternative Tools:**
    - **Evil-WinRM:** Simplifies remote interaction via Windows Remote Management (WinRM).

#### Defender's Perspective:

- **How could this be prevented?** Limit network exposure and use Just-In-Time (JIT) VM access.
- **Remediation:**
    - Enable **Azure Policy** to enforce secure VM configurations.
    - Use **Azure Bastion** for secure VM access without exposing public IPs.

---

### **Step 7: Privilege Escalation on Azure VM**

**Narrative:** The attacker enumerates the VM for privilege escalation opportunities.

**Command:**

```powershell
Invoke-RestMethod -Headers @{"Metadata"="true"} -Uri "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
```

#### Attacker's Perspective:

- **Why this approach?** Checks for metadata service exploitation or misconfigurations.
- **Advantages:** Identifies resource context for targeted attacks.
- **Alternative Tools:** Direct `curl` or other REST clients.

#### Defender's Perspective:

- **How could this be prevented?** Restrict access to the metadata service.
- **Remediation:**
    - Configure network security rules to block unauthorized access to `169.254.169.254`.
    - Monitor VM extensions using Azure Security Center recommendations.

## Links

https://devblogs.microsoft.com/devops/demystifying-service-principals-managed-identities/

https://github.com/itm4n/PrivescCheck

https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#authentication-administrator

https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/administrative-units