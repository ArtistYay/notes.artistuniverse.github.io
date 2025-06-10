Entra ID is a potential treasure trove for threat actors looking to gain access and increase privileges across the Microsoft Cloud. In this lab you'll learn about administrative units, dynamic security group membership, and leverage the powerful User Administrator role.

## Learning outcomes  

- Identify and use Azure SAS Token in Git repository
- Blob Storage enumeration and exfiltration
- Entra and administrative unit enumeration
- Leverage User Administrator permissions to abuse dynamic groups
- Identify and use GitHub deploy keys

### **Entry Point: GitHub Repository**

1. **Exposed SAS Token**: The public GitHub repository contained a sensitive file (`UploadResume.aspx.cs`) with an embedded Azure SAS token. This token enabled attackers to interact with the Azure Storage account.
    
    - **Impact**: Allowed access to candidate resumes and sensitive company documents, including an onboarding guide with a default password.
2. **Default Password Vulnerability**: The onboarding document revealed a default password for new hires, which was not enforced to be changed, providing a potential initial foothold.
    

---

### **Account Compromise: Credential Validation**

3. **Email Enumeration and Password Spraying**:
    - The attacker enumerated possible email addresses for a targeted user (e.g., Angelina Lee) and confirmed a valid user.
    - Using the default password, the attacker successfully authenticated as the user.

---

### **Azure Resource Enumeration: Privilege Escalation**

4. **Enumerating Entra ID**:
    
    - **Microsoft Graph Enumeration**: Discovered the compromised user was part of an **administrative unit** and had scoped **User Administrator** permissions.
    - **Role Misuse**: These permissions allowed resetting other users' passwords within the administrative unit.
5. **Compromising a Higher-Privilege User**:
    
    - The attacker reset the password of another user (Felix Schneider) with access to more resources.
    - Leveraging this user’s credentials, the attacker accessed an **Azure Key Vault**.

---

### **Dynamic Groups and Data Exfiltration**

6. **Abuse of Dynamic Groups**:
    
    - By modifying Felix's job title to match a **dynamic membership rule**, the attacker gained access to additional resources (e.g., "ALGO-ACCESS").
    - This access enabled the attacker to retrieve sensitive secrets, including a **GitHub deploy key** stored in the Key Vault.
7. **Exfiltrating the Secret Algorithm**:
    
    - Using the deploy key, the attacker cloned the private GitHub repository containing the company's proprietary algorithm and sensitive files.

---

### **Defense Analysis**

The root causes of this attack are primarily due to poor security practices and misconfigurations. Specific defenses include:

1. **GitHub Security**:
    
    - Regularly scan repositories for secrets (e.g., using tools like GitGuardian or GitHub Advanced Security).
    - Avoid embedding sensitive tokens or credentials in source code. Use environment variables or Azure Key Vault for secure storage.
2. **SAS Token Management**:
    
    - Limit permissions on SAS tokens (e.g., read-only for specific operations without `list` capability).
    - Rotate tokens regularly and avoid long-lived expiration dates.
    - Implement IP restrictions for SAS tokens.
3. **Default Passwords**:
    
    - Enforce password change policies for all new users.
    - Implement conditional access policies to prevent the use of default credentials.
4. **Entra ID Security**:
    
    - Scope administrative unit permissions minimally (e.g., least privilege).
    - Monitor changes in dynamic group membership and implement alerts for suspicious modifications.
5. **Azure Key Vault Security**:
    
    - Enforce fine-grained permissions for accessing secrets (e.g., separate read/write privileges).
    - Rotate secrets regularly and monitor access logs for anomalies.
6. **General Cloud Security Hygiene**:
    
    - Audit Azure resources and role assignments regularly.
    - Train employees on secure coding practices and the dangers of sensitive information exposure.


[https://www.mnemonic.io/no/resources/blog/abusing-dynamic-groups-in-azure-ad-for-privilege-escalation/](https://www.mnemonic.io/no/resources/blog/abusing-dynamic-groups-in-azure-ad-for-privilege-escalation/)

[https://blog.gitguardian.com/microsoft-ai-involuntarily-exposed-a-secret-giving-access-to-38tb-of-confidential-data-for-3-years/](https://blog.gitguardian.com/microsoft-ai-involuntarily-exposed-a-secret-giving-access-to-38tb-of-confidential-data-for-3-years/)

Automate the process of identifying administrative unit scoped role members and vulnerable users (Credit Ben Tamam): [https://raw.githubusercontent.com/BenTamam/PentestPlayground/refs/heads/main/Azure/Scripts/CheckScopedRolePrivileges.ps1](https://raw.githubusercontent.com/BenTamam/PentestPlayground/refs/heads/main/Azure/Scripts/CheckScopedRolePrivileges.ps1)

[https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview)

https://docs.github.com/v3/guides/managing-deploy-keys