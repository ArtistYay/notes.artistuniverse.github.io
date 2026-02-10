### **I. What is Meterpreter?**

- **Purpose:** An advanced payload in Metasploit that provides a powerful and interactive shell on compromised systems.
- **Functionality:** Offers a wide range of post-exploitation capabilities, including file system navigation, process manipulation, privilege escalation, and pivoting.
- **Versions:** Different versions exist for various target systems and architectures, providing specialized functionalities.
### **II. How Meterpreter Works:**

- **In-Memory Execution:** Meterpreter runs entirely in memory, avoiding writing itself to disk. This makes it stealthier and less likely to be detected by traditional antivirus scans that focus on file system activity.
- **Encrypted Communication:** Uses encrypted communication channels (typically TLS) to avoid detection by network-based intrusion detection and prevention systems (IDS/IPS). This can bypass security measures that rely on analyzing unencrypted network traffic.
- **Process Spoofing:** Meterpreter often disguises itself as a legitimate process to further evade detection. It might inject itself into an existing process or masquerade as a common system service.
### **III. Meterpreter Payloads:**

- **Types:**
    - **Staged:** Smaller initial payload that downloads the full Meterpreter stage.
    - **Inline:** The entire Meterpreter payload is delivered at once.
- **Versions:** Numerous versions exist for various platforms and architectures (e.g., Windows, Linux, Android, macOS).
- **Choosing a Version:** Consider the target operating system, available components (e.g., Python, PHP), and network restrictions when selecting a Meterpreter payload.
### **IV. Meterpreter Commands:**

- **`help`:** Displays the help menu with available commands.
- **Core Commands:**
    - **`background`:** Backgrounds the current session.
    - **`exit`:** Terminates the Meterpreter session.
    - **`guid`:** Gets the session's globally unique identifier (GUID).
    - **`info`:** Displays information about a post-exploitation module.
    - **`load`:** Loads Meterpreter extensions.
    - **`migrate`:** Migrates Meterpreter to a different process.
    - **`run`:** Executes a Meterpreter script or post module.
    - **`sessions`:** Switches between active sessions.
- **File System Commands:**
    - **`cd`:** Changes the current directory.
    - **`ls` or `dir`:** Lists files in the directory.
    - **`pwd`:** Prints the current working directory.
    - **`edit`:** Edits a file.
    - **`cat`:** Displays the contents of a file.
    - **`rm`:** Deletes a file.
    - **`search`:** Searches for files.
    - **`upload`:** Uploads files or directories.
    - **`download`:** Downloads files or directories.
- **Networking Commands:**
    - **`arp`:** Displays the ARP cache.
    - **`ifconfig`:** Shows network interface information.
    - **`netstat`:** Lists network connections.
    - **`portfwd`:** Sets up port forwarding.
    - **`route`:** Views and modifies routing tables.
- **System Commands:**
    - **`clearev`:** Clears event logs.
    - **`execute`:** Executes a command on the target.
    - **`getpid`:** Gets the Meterpreter process ID.
    - **`getuid`:** Gets the user that Meterpreter is running as.
    - **`kill`:** Terminates a process.
    - **`ps`:** Lists running processes.
    - **`reboot`:** Reboots the target.
    - **`shell`:** Spawns a system command shell.
    - **`shutdown`:** Shuts down the target.
    - **`sysinfo`:** Gets system information (OS, architecture, etc.).
- **Other Commands:**
    - **`idletime`:** Gets user idle time.
    - **`keyscan_start`, `keyscan_stop`, `keyscan_dump`:** Keystroke logging.
    - **`screenshare`:** Shares the target's screen.
    - **`screenshot`:** Takes a screenshot.
    - **`record_mic`:** Records audio.
    - **`webcam_chat`, `webcam_list`, `webcam_snap`, `webcam_stream`:** Webcam control.
    - **`getsystem`:** Attempts privilege escalation to SYSTEM.
    - **`hashdump`:** Dumps password hashes from the SAM database (Windows).
### **V. Example Meterpreter Usage:**

- **`getuid`:** Check the current user privileges.
- **`ps`:** List running processes to identify potential migration targets.
- **`migrate [PID]`:** Migrate to a different process (e.g., for keylogging or stability).
- **`hashdump`:** Dump password hashes.
- **`search -f [filename]`:** Search for specific files.
- **`shell`:** Spawn a system command shell.
### **VI. Key Considerations:**

- **Antivirus Evasion:** While Meterpreter employs techniques to avoid detection, it's not foolproof. Modern antivirus and endpoint detection and response (EDR) solutions may still detect it.
- **Privilege Level:** Be mindful of the user context Meterpreter is running in. Migrating to a lower-privileged process can result in losing access.
- **Stability:** Meterpreter sessions can be unstable, especially when migrating to different processes.
- **Network Traffic:** Meterpreter's encrypted communication can still generate network traffic that might raise suspicion.