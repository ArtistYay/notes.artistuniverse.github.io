Learn how to use the GraphRunner Microsoft 365 post-exploitation toolset, and how it can be used to loot data from Exchange Online, Teams, SharePoint and OneDrive. You'll also get hands-on experience with MFASweep, PowerShell and Azure SQL Database.

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

This lab demonstrates a typical attack story, highlighting the risks associated with weak or incomplete security configurations in hybrid cloud environments like Azure and Microsoft 365. Here's the attack breakdown:

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

### **Why This Scenario Matters for Cloud Security Engineers**

As a cloud security engineer, this scenario is a real-world example of how attackers pivot from compromised cloud credentials to accessing sensitive on-premise and cloud-hosted resources. It emphasizes the importance of understanding:

- Security configurations for hybrid cloud environments.
- Microsoft Graph API exploitation methods.
- Tools like MFASweep and GraphRunner.
- Proactive defense strategies to prevent lateral movement and sensitive data exfiltration.
---

**Look up what these scripts mean**: 
`$conn = New-Object System.Data.SqlClient.SqlConnection $password='$reporting$123' $conn.ConnectionString = "Server=mbt-finance.database.windows.net;Database=Finance;User ID=financereports;Password=$password;" $conn.Open()

`$sqlcmd = $conn.CreateCommand() $sqlcmd.Connection = $conn $query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';" $sqlcmd.CommandText = $query $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd $data = New-Object System.Data.DataSet $adp.Fill($data) | Out-Null $data.Tables

These scripts represent a sequence of **PowerShell commands** used to connect to an **Azure SQL Database**, execute a query, and fetch data. Here's a breakdown of what each part of the script does:
### **Step-by-Step Explanation**

1. **Create a SQL Connection Object:**
    
    powershell
    
    Copy code
    
    `$conn = New-Object System.Data.SqlClient.SqlConnection`
    
    - Creates a new object of type `SqlConnection` from the `System.Data.SqlClient` namespace.
    - This object will represent a connection to the Azure SQL database.
2. **Set the Database Connection String:**
    
    powershell
    
    Copy code
    
    `$password = '$reporting$123' $conn.ConnectionString = "Server=mbt-finance.database.windows.net;Database=Finance;User ID=financereports;Password=$password;"`
    
    - Defines the connection string with:
        - **Server:** The database server address (`mbt-finance.database.windows.net`).
        - **Database:** The specific database to connect to (`Finance`).
        - **User ID:** The username for authentication (`financereports`).
        - **Password:** The password for authentication (`$reporting$123`).
3. **Open the SQL Connection:**
    
    powershell
    
    Copy code
    
    `$conn.Open()`
    
    - Opens the connection to the Azure SQL database, allowing the script to interact with it.
### **Executing a Query**

4. **Create a Command Object:**
    
    powershell
    
    Copy code
    
    `$sqlcmd = $conn.CreateCommand() $sqlcmd.Connection = $conn`
    
    - Creates a SQL command object that will execute queries on the open connection.
5. **Define the Query:**
    
    powershell
    
    Copy code
    
    `$query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';" $sqlcmd.CommandText = $query`
    
    - The `CommandText` property specifies the SQL query to execute:
        - Retrieves a list of all **base tables** in the database schema (tables created by users, not system tables).
        - `INFORMATION_SCHEMA.TABLES` is a metadata view that contains details about all tables in the database.
6. **Prepare to Retrieve the Data:**
    
    powershell
    
    Copy code
    
    `$adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd $data = New-Object System.Data.DataSet`
    
    - `SqlDataAdapter`: A .NET object used to fetch data from the database.
    - `DataSet`: An in-memory representation of the data retrieved.
7. **Fetch the Data:**
    
    powershell
    
    Copy code
    
    `$adp.Fill($data) | Out-Null $data.Tables`
    
    - Executes the query (`$adp.Fill`) and stores the results in the `$data` dataset.
    - Outputs the retrieved tables from `$data.Tables`.
### **Purpose of the Script**

1. **Connection:** Establishes a connection to the Azure SQL database.
2. **Query Execution:** Executes a SQL query to list all base tables in the database.
3. **Data Retrieval:** Retrieves and stores the results for further processing.
### **Why It's Significant in the Lab**

This script demonstrates how an attacker can:

- Use stolen credentials to connect to an Azure SQL database.
- Enumerate database tables to discover sensitive information.
- Later, execute further queries to extract data from specific tables.

As a **cloud security engineer**, you should:

1. Enforce **least privilege access** to databases.
2. Ensure that sensitive data is encrypted in transit and at rest.
3. Monitor and alert on unusual database connections or queries.
4. Limit database access to trusted IP ranges using **firewall rules**.
--- 

https://www.blackhillsinfosec.com/exploiting-mfa-inconsistencies-on-microsoft-services/