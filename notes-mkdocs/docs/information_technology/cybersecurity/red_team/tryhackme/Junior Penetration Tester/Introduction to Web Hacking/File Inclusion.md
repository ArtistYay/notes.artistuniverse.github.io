### **I. What is File Inclusion?**

- Vulnerability where attackers can include unexpected files into a web application.
- Often due to poor input validation.
- **Types:**
    - Local File Inclusion (LFI): Includes files from the same server.
    - Remote File Inclusion (RFI): Includes files from a remote server.
- **Risks:**
    - Data leakage (code, credentials).
    - Remote Code Execution (RCE).
### **II. Path Traversal:**

- Also known as Directory Traversal.
- Reading files outside the web application's root directory.
- Exploits by manipulating the URL.
- _Example:_ `http://webapp.thm/get.php?file=../../../../etc/passwd`

   ![screenshot](../../../images/Pasted image 20250211204441.png)

- **Common OS Files to Target:** `/etc/passwd`, `/etc/shadow`, `/proc/version`, etc. (Linux), `C:\boot.ini` (Windows)
![screenshot](../../../images/Pasted image 20250211204400.png)

### **III. Local File Inclusion (LFI):**

- Often occurs with PHP functions like `include`, `require`, `include_once`, `require_once`.
- **Exploitation:** Similar to path traversal, but the included file's code is executed.
- **Bypassing Filters:**
    - **Null Byte (%00):** Terminates strings, can bypass filters in older PHP versions (before 5.3.4).
    - **Current Directory Trick:** Using `/..` to move up directories.
    - **Double Encoding:** Encoding `../` twice to bypass filters.
- **Error Messages:** Can reveal the include function's structure and the web application's directory path.
### **IV. Remote File Inclusion (RFI):**

- Includes files from a remote server.
- Requires `allow_url_fopen` to be enabled in PHP.
- **Higher Risk:** Can lead to RCE.
- **Other Consequences:** Sensitive information disclosure, Cross-Site Scripting (XSS), Denial of Service (DoS).
- **Attack Steps:**
    1. Attacker hosts malicious file on their server.
    2. Attacker injects the URL of the malicious file into the vulnerable parameter.
    3. Web server fetches and executes the remote file.
     ![screenshot](../../../images/Pasted image 20250211204253.png)

### **V. Preventing File Inclusion Vulnerabilities:**

- Keep systems and frameworks updated.
- Disable PHP errors in production.
- Use a Web Application Firewall (WAF).
- Disable unnecessary PHP features (`allow_url_fopen`, `allow_url_include`).
- Validate user input.
- Implement whitelisting and blacklisting.
- Use parameterized queries/prepared statements.
- Principle of Least Privilege.