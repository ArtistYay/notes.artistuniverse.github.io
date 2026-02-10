### I. Telnet

- **Purpose:** Remote terminal access.
- **Protocol:** Telnet.
- **Port:** 23 (TCP).
- **Insecure:** Sends data in cleartext (unencrypted), including usernames and passwords.
- **Vulnerable to eavesdropping:** Attackers can easily capture credentials from network traffic.
- **Example:** `telnet <machine_ip>`
### II. Hypertext Transfer Protocol (HTTP)

- **Purpose:** Transfer web pages and other web resources.
    
- **Cleartext Protocol:** Sends data unencrypted.
    
- **Can be interacted with using Telnet:** Manually send `GET` requests to retrieve web pages.
    
- **Example:**
    
    ```
    telnet <machine_ip> 80
    GET /index.html HTTP/1.1
    Host: <any_value>
    ```
    
- **Web Servers:**
    
    - Apache: [https://www.apache.org/](https://www.apache.org/)
    - IIS: [https://www.iis.net/](https://www.iis.net/)
    - nginx: [https://nginx.org/](https://nginx.org/)
- **Web Browsers:**
    
    - Chrome, Edge, Firefox, Safari, etc.
### III. File Transfer Protocol (FTP)

- **Purpose:** Transfer files between computers.
    
- **Cleartext Protocol:** Sends data unencrypted, including login credentials.
    
- **Can be partially interacted with using Telnet:** Can log in and execute some commands, but not transfer files.
    
- **Two Modes:**
    
    - Active: Data transfer originates from server (port 20).
    - Passive: Data transfer originates from client (port > 1023).
- **Example:**
    
    ```
    telnet <machine_ip> 21
    USER <username>
    PASS <password>
    ```
    
- **FTP Servers:**
    
    - vsftpd: [https://security.appspot.com/vsftpd.html](https://security.appspot.com/vsftpd.html)
    - ProFTPD: [http://www.proftpd.org/](http://www.proftpd.org/)
    - uFTP: [https://www.uftpserver.com/](https://www.uftpserver.com/)
- **FTP Clients:**
    
    - Console FTP client (Linux)
    - FileZilla: [https://filezilla-project.org/](https://filezilla-project.org/)
    - Web browsers (limited support)
### IV. Simple Mail Transfer Protocol (SMTP)

- **Purpose:** Send email.
- **Mail User Agent (MUA):** Email client (e.g., Thunderbird, Outlook).
- **Mail Transport Agent (MTA):** Server that sends email.
### V. Post Office Protocol 3 (POP3)

- **Purpose:** Receive email.
- **Downloads emails to local device:** Emails are deleted from the server after download.
### VI. Internet Message Access Protocol (IMAP)

- **Purpose:** Receive email.
- **Synchronizes email across devices:** Emails are stored on the server and can be accessed from multiple devices.