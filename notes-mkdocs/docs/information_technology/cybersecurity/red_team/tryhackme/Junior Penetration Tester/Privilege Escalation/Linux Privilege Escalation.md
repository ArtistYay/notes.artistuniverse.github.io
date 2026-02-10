### **I. What is Privilege Escalation?**

- **Definition:** Exploiting vulnerabilities or misconfigurations to gain higher-level permissions than initially granted.
- **Importance:**
    - Initial access rarely provides administrative rights.
    - Allows actions like resetting passwords, accessing protected data, modifying configurations, establishing persistence.
### **II. Enumeration:**

- **Purpose:** Gathering information about the system to identify potential privilege escalation vectors.
- **Commands and Techniques:**
    - **`hostname`:** Reveals the system's hostname, which may indicate its role.
    - **`uname -a`:** Displays kernel version information, useful for finding kernel exploits.
    - **`/proc/version`:** Provides details about the kernel and compiler (if present).
    - **`/etc/issue`:** Contains system identification information.
    - **`ps`:** Lists running processes.
        - `ps -A`: All processes.
        - `ps axjf`: Process tree.
        - `ps aux`: Processes for all users, including those not attached to a terminal.
    - **`env`:** Displays environment variables, including `PATH` (which might contain useful tools).
    - **`sudo -l`:** Lists commands the current user can run with `sudo`.
    - **`ls -la`:** Lists files and directories, including hidden ones, with detailed permissions.
    - **`id`:** Shows user ID, group memberships, and effective user ID.
    - **`/etc/passwd`:** Contains information about user accounts.
    - **`history`:** Displays command history, which may reveal sensitive information.
    - **`ifconfig`:** Shows network interface configuration, potentially revealing other network segments.
    - **`ip route`:** Displays routing table information.
    - **`netstat`:** Provides information about network connections and listening ports.
        - `netstat -a`: All connections.
        - `netstat -l`: Listening ports.
        - `netstat -s`: Network statistics.
        - `netstat -tp`: Connections with process IDs.
        - `netstat -i`: Interface statistics.
        - `netstat -ano`: All connections with process IDs and timers.
    - **`find`:** A powerful command for searching files and directories based on various criteria (name, permissions, size, modification time, etc.).
    - **Automated Tools:**
        - LinPeas
        - LinEnum
        - LES (Linux Exploit Suggester)
        - Linux Smart Enumeration
        - Linux Priv Checker
### **III. Kernel Exploits:**

- **Process:**
    1. Identify the kernel version.
    2. Search for a matching exploit.
    3. Execute the exploit.
- **Considerations:**
    - Kernel exploits can be risky and lead to system instability.
    - Carefully analyze the exploit code before execution.
    - Ensure proper setup and execution (may require additional steps).
### **IV. Exploiting Sudo Rights:**

- **`sudo -l`:** Check for commands the user can run with `sudo`.
- **GTFOBins:** A valuable resource for identifying ways to exploit sudo permissions for various binaries.
- **Example (Apache2):** `sudo apache2 -f /etc/shadow` (leaks the first line of `/etc/shadow`).
### **V. Exploiting LD_PRELOAD:**

- **LD_PRELOAD:** An environment variable that allows preloading shared libraries.
- **Conditions:** Requires the `env_keep` option to be enabled and the real user ID to match the effective user ID.
- **Steps:**
    1. Check for `LD_PRELOAD` and `env_keep`.
    2. Write a C program that spawns a shell.
    3. Compile the program as a shared object (`.so`).
    4. Run a `sudo` command with `LD_PRELOAD` pointing to the shared object.
### **VI. Exploiting SUID/SGID Bits:**

- **SUID (Set-user ID):** Allows a file to be executed with the owner's permissions.
- **SGID (Set-group ID):** Allows a file to be executed with the group's permissions.
- **Finding SUID/SGID Files:** `find / -type f -perm -04000 -ls 2>/dev/null`
- **GTFOBins:** Provides information on exploiting SUID/SGID binaries.
- **Example (nano):** If `nano` has the SUID bit set, it can be used to read sensitive files (e.g., `/etc/shadow`) or modify system files (e.g., `/etc/passwd`).
### **VII. Exploiting Cron Jobs:**

- **Cron Jobs:** Scheduled tasks that run with the owner's privileges.
- **Crontab:** Stores cron job configurations.
- **Exploitation:**
    1. Identify cron jobs running with root privileges.
    2. Modify the script or command executed by the cron job to gain root access.
- **Example:** Replace a script executed by a root cron job with a reverse shell payload.
### **VIII. Exploiting PATH:**

- **PATH:** An environment variable that specifies directories where the system searches for executables.
- **Exploitation:**
    1. Identify writable directories in the `PATH`.
    2. Create a malicious executable with the same name as a privileged program.
    3. Place the malicious executable in the writable directory.
    4. When the privileged program is executed, the malicious version will be run instead.
### **IX. Exploiting NFS:**

- **NFS (Network File System):** Allows sharing files and directories over a network.
- **`/etc/exports`:** NFS configuration file.
- **`no_root_squash`:** A risky option that disables root squashing (mapping root to a less privileged user).
- **Exploitation:**
    1. Identify NFS shares with `no_root_squash` enabled.
    2. Mount the share on the attacking machine.
    3. Create a malicious executable with the SUID bit set.
    4. Execute the file on the target system through the NFS share.
### **X. Key Takeaways:**

- Privilege escalation is a crucial step in penetration testing.
- Thorough enumeration is essential for identifying potential vulnerabilities and misconfigurations.
- Various techniques and tools can be used to escalate privileges, depending on the target system's configuration and vulnerabilities.
- Always prioritize maintaining the integrity of the target system during real-world engagements.