*Get an introduction to one of the most popular Azure services - Blob Storage, and show how attackers can use it to access secrets and get a foothold in a cloud environment.*

## Learning outcomes  

- Familiarity with the Azure CLI
- Identification and enumeration of Azure Blob Container
- Leverage blob previous version functionality to reveal secrets
## Notes

- This command `Invoke-WebRequest -Uri 'https://mbtwebsite.blob.core.windows.net/$web/index.html' -Method Head` is getting the header of the website.
- Adding the ` | Select-Object -ExpandProperty Headers` at the end expands the headers.
- On Linux it's `curl -I <website>` 
- `https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list` returns all the blobs in a XML document
- The `/` in the URL `https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list&delimiter=%2F` gets the directory in the blob container.
- The `include` in the URL `https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list&include=versions` lists the versions but it's only supported by version `2019-12-12` and later [URI parameters](https://learn.microsoft.com/en-us/rest/api/storageservices/list-blobs?tabs=microsoft-entra-id#uri-parameters)
- You can read more about [previous Azure Storage versions](https://learn.microsoft.com/en-us/rest/api/storageservices/previous-azure-storage-service-versions)
- We went ahead and used curl to list the versions of the directory `curl -H "x-ms-version: 2019-12-12" 'https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list&include=versions' | xmllint --format - | less` we listed it in a xml format and less.
- Went ahead and downloaded the zip file we seen using the version ID `curl -H "x-ms-version: 2019-12-12" 'https://mbtwebsite.blob.core.windows.net/$web/scripts-transfer.zip?versionId=2024-03-29T20:55:40.8265593Z'  --output scripts-transfer.zip`

[38TB of data accidentally exposed by Microsoft AI researchers](https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers)

[Circle K US spills partial credit card details, among other sensitive data](https://cybernews.com/security/circlek-leak-credit-card-exposed/)

The attack scenario described demonstrates a realistic and multi-step security assessment of an Azure Blob Storage misconfiguration that culminates in compromising sensitive credentials and gaining access to critical cloud resources. Here’s a breakdown of the **attack story**:

---

### **Attack Story**

#### **Phase 1: Discovery**

1. **Reconnaissance:**
    
    - The attackers identified a public URL (`https://mbtwebsite.blob.core.windows.net/$web/index.html`) from documentation.
    - By examining the response headers, they confirmed that the resource was hosted on Azure Blob Storage.
2. **Enumeration:**
    
    - By manipulating the URL (`https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list`), the attackers enumerated the public blob container.
    - This exposed available files and confirmed that the container was publicly accessible.
3. **Blob Versioning Abuse:**
    
    - They checked for blob versioning using advanced Azure-specific HTTP headers (e.g., `x-ms-version`).
    - Previous versions of sensitive files, including `scripts-transfer.zip`, were identified and downloaded.

---

#### **Phase 2: Exploitation**

1. **File Analysis:**
    
    - Inside the downloaded `scripts-transfer.zip`, PowerShell scripts were found. These scripts contained **hardcoded credentials** for both:
        - **Active Directory** (`MegaBigTech123!` for `marcus_adm`).
        - **Entra ID (Azure AD)** (`TheEagles12345!` for `marcus@megabigtech.com`).
2. **Privilege Escalation:**
    
    - The script `entra_users.ps1` was executed, enabling the attacker to authenticate to Azure using `Connect-AzAccount`.
    - Once authenticated, the script retrieved and listed all users in Entra ID via the Microsoft Graph API.
3. **Foothold in Cloud Environment:**
    
    - With valid Azure credentials and access tokens, the attackers established a foothold in Mega Big Tech’s Azure tenant, enabling further enumeration and lateral movement.

---

### **Key Lessons and Real-World Context**

1. **Public Blob Storage Misconfiguration:**
    
    - Similar to S3 bucket misconfigurations in AWS, public Azure Blob Storage containers have caused breaches when sensitive data was inadvertently exposed.
2. **Blob Versioning Risk:**
    
    - Attackers leveraged the **Blob Storage versioning** feature to retrieve deleted or outdated files. While this feature is designed for resilience, improper configuration exposed sensitive historical data.
3. **Hardcoded Credentials:**
    
    - Storing credentials in scripts or code is a critical error. This provides attackers with a direct route to compromise.
4. **Real-World Example:**
    
    - Data breaches such as the Capital One incident in 2019 highlight the danger of misconfigured cloud resources and inadequate secret management practices.

---

### **Defense Story**

#### **Mitigation Steps**

1. **Restrict Public Access to Blob Storage:**
    
    - Use Azure’s **Shared Access Signatures (SAS)** or private access policies to limit access to only necessary resources.
2. **Secure Blob Versioning:**
    
    - Configure versioning settings to ensure sensitive files are not inadvertently exposed. Periodically review and delete obsolete or sensitive versions of blobs.
3. **Remove Hardcoded Credentials:**
    
    - Store credentials in **Azure Key Vault** or another PAM solution. Replace plaintext credentials in scripts with secure retrieval methods using Key Vault APIs.
4. **Automate Misconfiguration Detection:**
    
    - Regularly scan and monitor blob containers using tools like Microsoft Defender for Storage or custom scripts to identify public access or sensitive data leaks.

#### **Incident Response**

- Revoking compromised credentials for `marcus_adm` and `marcus@megabigtech.com`.
- Rotating Azure access tokens and enforcing MFA.
- Reviewing and reconfiguring the security posture of all storage accounts to prevent future misconfigurations.