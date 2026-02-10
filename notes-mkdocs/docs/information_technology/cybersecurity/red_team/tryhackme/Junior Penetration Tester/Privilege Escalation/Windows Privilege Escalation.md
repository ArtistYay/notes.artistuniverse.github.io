### **I. What is Privilege Escalation?**

- **Definition:** Exploiting weaknesses in a system to gain access to accounts with higher privileges.
- **Goal:** Typically, to gain administrative rights, but may involve escalating to other user accounts first.
- **Weaknesses to Exploit:**
    - Misconfigurations (services, tasks).
    - Excessive user privileges.
    - Vulnerable software.
    - Missing security patches.
### **II. Windows User Account Types:**

- **Administrators:** Highest privileges, can change system settings and access all files.
- **Standard Users:** Limited privileges, can only perform basic tasks and access their own files.
- **Special Accounts:**
    - **SYSTEM/LocalSystem:** Used by the OS, has the highest level of access.
    - **Local Service:** Runs services with minimal privileges, uses anonymous network connections.
    - **Network Service:** Runs services with minimal privileges, uses computer account for network authentication.
### **III. Finding Credentials:**

- **Unattended Installations:** Check for unattended installation files that may contain administrator credentials (e.g., `C:\Unattend.xml`, `C:\Windows\Panther\Unattend.xml`).
- **PowerShell History:** `type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt`
- **Saved Credentials:** `cmdkey /list`, `runas /savecred /user:admin cmd.exe`
- **IIS Configuration:** Check `web.config` files for database connection strings or authentication credentials.
- **Software:** Many applications store credentials (e.g., PuTTY stores proxy credentials in the registry).
### **IV. Exploiting Misconfigurations:**

- **Scheduled Tasks:**
    - Check scheduled tasks for insecure permissions or the ability to modify the executed command.
    - Use `schtasks` to list and query tasks.
    - Use `icacls` to check permissions on task executables.
- **AlwaysInstallElevated:** (Informational) A registry setting that allows MSI files to run with elevated privileges.
- **Insecure Service Permissions:**
    - Check service permissions with `sc qc [service_name]`.
    - Use `icacls` to check permissions on service executables.
    - If the executable has weak permissions, replace it with a malicious payload (e.g., a reverse shell).
- **Unquoted Service Paths:**
    - Exploit the way the Service Control Manager (SCM) handles unquoted service paths.
    - If a service path contains spaces and is not quoted, the SCM may execute a different executable.
    - Place a malicious executable in a location that will be searched by the SCM.
- **Insecure Service DACL:**
    - If the service's DACL allows modification, reconfigure the service to execute a malicious payload with higher privileges (e.g., SYSTEM).
    - Use `accesschk64.exe` to check service DACLs.
    - Use `sc config` to modify service configurations.
### **V. Exploiting Windows Privileges:**

- **`whoami /priv`:** Lists user privileges.
- **Priv2Admin:** A resource for identifying exploitable privileges.
- **`SeBackup` and `SeRestore`:**
    - Allows reading and writing any file, bypassing DACLs.
    - Can be used to copy SAM and SYSTEM registry hives to extract password hashes.
    - Use `reg save` to backup registry hives.
    - Use `secretsdump.py` to extract hashes.
- **`SeTakeOwnership`:**
    - Allows taking ownership of any file or object.
    - Can be used to replace `utilman.exe` with a command prompt, gaining SYSTEM access.
    - Use `takeown` to take ownership.
    - Use `icacls` to grant permissions.
- **`SeImpersonate` and `SeAssignPrimaryToken`:**
    - Allows impersonating other user accounts.
    - Can be exploited to gain access to privileged accounts (e.g., SYSTEM).
    - RogueWinRM is a tool that can exploit this privilege.
### **VI. Unpatched Software:**

- **`wmic product get name,version,vendor`:** Lists installed software and versions.
- **Research:** Search for exploits for known vulnerabilities in installed software.
- **Example (Druva inSync):** A vulnerable RPC server allows executing arbitrary commands with SYSTEM privileges.
### **VII. Automated Tools:**

- **WinPEAS:** A script for enumerating Windows systems and identifying privilege escalation vectors.
- **PrivescCheck:** A PowerShell script that checks for common privilege escalation vulnerabilities.
- **WES-NG:** Runs on the attacker's machine and suggests exploits based on `systeminfo` output from the target.
- **Metasploit:** The `multi/recon/local_exploit_suggester` module can suggest exploits for Meterpreter sessions.