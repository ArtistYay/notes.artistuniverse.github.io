### **I. What is Command Injection?**

- Exploiting an application to execute OS commands with the application's privileges.
- Also known as Remote Code Execution (RCE).
- _Example:_ Command injection on a web server running as user "joe" executes commands as "joe."
### **II. Discovering Command Injection:**

- **How it Works:** Programming languages use functions to make system calls. User input is passed to these functions, creating the vulnerability.
- **Example Scenario:**
    1. Application stores MP3 files.
    2. User inputs a song title (`$title` variable).
    3. `$title` is passed to `grep` to search `songtitle.txt`.
    4. Output determines if the song exists. _Vulnerability:_ User input is directly used in the command.
    
![screenshot](../../../images/Pasted image 20241114122730.png)

### **III. Exploiting Command Injection:**

- **Command Combination:** Use shell operators (`;`, `&`, `&&`) to execute multiple commands at once. `&&` does not work on Windows.
- **Detection Methods:**
    - **Blind:** No direct output. Investigate application behavior.
        - Use `ping` or `sleep` for time delays.
        - Redirect output with `>`.
        - Use `curl` for out-of-band communication.
    - **Verbose:** Direct feedback from the application. _Example:_ `whoami` reveals the user the application runs as.
### **IV. Remediating Command Injection:**

- **Vulnerable Functions:** Avoid using functions that directly interact with the OS (e.g., `exec()`, `passthru()`, `system()` in PHP).
- **Input Validation:** Sanitize user input.
    - Specify accepted data formats/types (e.g., only numerical data).
    - Remove special characters (`>`, `&`, `/`).
	
    ![screenshot](../../../images/Pasted image 20241114130743.png)
    ![screenshot](../../../images/Pasted image 20241114130825.png)

- **Whitelisting:** Use a whitelist of allowed characters or inputs. This is much better than blacklisting.
- **Parameterization/Prepared Statements:** Treat user input as data, not as commands. This is the most effective defense.
- **Principle of Least Privilege:** Run applications with minimal necessary privileges. Limit the impact of a successful command injection attack.
- **Encoding:** Encode user input to prevent special characters from being interpreted as commands.