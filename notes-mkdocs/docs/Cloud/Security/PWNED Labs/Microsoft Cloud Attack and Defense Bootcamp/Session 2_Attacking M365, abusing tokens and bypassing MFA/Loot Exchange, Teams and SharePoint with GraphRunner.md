*Learn how to use the GraphRunner Microsoft 365 post-exploitation toolset, and how it can be used to loot data from Exchange Online, Teams, SharePoint and OneDrive. You'll also get hands-on experience with MFASweep, PowerShell and Azure SQL Database.*

## Learning outcomes  

- Use MFASweep to identify MFA enablement gaps
- Exfiltrate data from SharePoint, Teams and Exchange Online
- Move laterally and pillage data from Azure SQL database

## Notes

- Get the MFASweep script a Github repo `git clone https://raw.githubusercontent.com/dafthack/MFASweep/master/MFASweep.ps1`
- MFASweep gets the status of MFA on various online Microsoft services. `Invoke-MFASweep -Username Clara.Miller@megabigtech.com -Password MegaBigTech99 -Recon -IncludeADFS` 
- To get the license of a user run `Get-MgUserLicenseDetail -UserId "Clara.Miller@megabigtech.com"`
- An excellent tool for finding loot in Microsoft 365 environments is the `GraphRunner` post-exploitation toolset. Learn more with this [video](https://www.youtube.com/watch?v=o29jzC3deS0&ab_channel=BlackHillsInformationSecurity) and [blog post](https://www.blackhillsinfosec.com/introducing-graphrunner/)
- To get a list of the modules that can be ran in GraphRunner utilize the `List-GraphRunnerModules` command
- You can also get examples of how to use the module with `Get-Help Invoke-SearchSharePointAndOneDrive -examples`
- Always start with `Get-GraphTokens`
- Database.windows.net is a fully qualified server name for an Azure SQL Database
- Interact with the SQL database with:

---

### **Attack Flow**

1. **Initial Compromise:**
    
    - Credentials were stolen via phishing, granting access to Microsoft 365 and Azure services.
    - No Multi-Factor Authentication (MFA) was enforced, making it easy for the attacker to authenticate with just a username and password.
2. **Reconnaissance:**
    
    - **MFASweep** was used to enumerate Microsoft services and identify where MFA was not enabled.
    - The attacker discovered that the user could access Microsoft Graph and Service Management APIs without MFA.
3. **Exfiltration of Microsoft 365 Data:**
    
    - Using **GraphRunner**, the attacker:
        - Enumerated user licenses and discovered access to productivity apps like SharePoint, Teams, and Outlook.
        - Searched for sensitive files (e.g., passwords, financial documents) in SharePoint and OneDrive.
        - Extracted sensitive information from Teams messages and mailbox searches.
4. **Lateral Movement and Database Compromise:**
    
    - Credentials for an Azure SQL Database were found in an email.
    - Using PowerShell, the attacker connected to the Azure SQL Database.
    - The database contained unencrypted Personally Identifiable Information (PII) of customers, including financial data.
5. **Data Pillaging:**
    
    - Extracted all rows from the `Subscribers` table, gaining access to sensitive subscriber information.
    - Demonstrated the business impact by exfiltrating PII, financial data, and database structure details.

---

### **Key Takeaways:**

1. **Attack Objectives:**
    
    - **Goal:** Access customer records and demonstrate business impact.
    - The attacker exploited weak security practices, such as no MFA, exposed database services, and poor data governance (e.g., sensitive info in emails and documents).
2. **Key Tools & Techniques:**
    
    - **MFASweep:** To identify where MFA was missing.
    - **GraphRunner:** To exploit Microsoft 365 APIs for data exfiltration.
    - **SQL Queries via PowerShell:** To connect to and extract data from an Azure SQL Database.
3. **Lessons for Defense:**
    
    - **Enforce MFA:** Ensure all services, including Graph API and Service Management APIs, require MFA for access.
    - **Minimize Access:** Implement least privilege principles for data and services.
    - **Secure Sensitive Data:**
        - Avoid sharing credentials via email, chat, or unprotected files.
        - Encrypt sensitive information in databases.
    - **Restrict Network Access:** Azure SQL should have firewall rules limiting access to specific IP ranges.
    - **Monitor Activity:** Regularly audit access logs, API activity, and database queries for suspicious behavior.

---

## Links

[Exploiting MFA Inconsistencies on Microsoft Services](https://www.blackhillsinfosec.com/exploiting-mfa-inconsistencies-on-microsoft-services/)