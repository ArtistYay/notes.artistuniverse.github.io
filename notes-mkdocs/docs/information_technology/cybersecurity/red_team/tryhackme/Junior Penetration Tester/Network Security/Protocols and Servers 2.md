## Network Security & Mitigation - Detailed Notes

### I. Security Triad (CIA)

  * **Confidentiality:** Keeping data secret and accessible only to authorized parties.
  * **Integrity:** Ensuring data accuracy, consistency, and completeness.
  * **Availability:** Ensuring systems and services are accessible when needed.
### II. Attacks (DAD)

  * **Disclosure:** Unauthorized access to confidential information.
  * **Alteration:** Unauthorized modification of data.
  * **Destruction:** Loss of data or disruption of service.
### III. Sniffing Attacks

  * **Definition:** Capturing network traffic to analyze data.
  * **Tools:**
      * Tcpdump: [https://www.tcpdump.org/](https://www.google.com/url?sa=E&source=gmail&q=https://www.tcpdump.org/) (command-line)
      * Wireshark: [https://www.wireshark.org/](https://www.google.com/url?sa=E&source=gmail&q=https://www.wireshark.org/) (GUI)
      * Tshark: [https://www.wireshark.org/\#tshark](https://www.google.com/search?q=https://www.wireshark.org/%23tshark) (command-line, part of Wireshark)
  * **Vulnerable Protocols:** Any protocol that sends data in cleartext (Telnet, HTTP, FTP, SMTP, POP3, IMAP).
  * **Mitigation:** Encryption (TLS, SSH).
### IV. Man-in-the-Middle (MITM) Attacks

  * **Definition:** An attacker intercepts communication between two parties, relaying and potentially modifying messages.
  * **Tools:** Ettercap, Bettercap.
  * **Vulnerable Protocols:** Cleartext protocols (HTTP, FTP, SMTP, POP3).
  * **Mitigation:**
      * Encryption (TLS).
      * Strong authentication.
      * Message integrity checks (digital signatures).
### V. Transport Layer Security (TLS)

  * **Purpose:** Secure communication over a network.
  * **Successor to SSL:** More secure, widely adopted.
  * **Encrypts data:** Protects confidentiality.
  * **Verifies server identity:** Prevents MITM attacks.
  * **Ensures data integrity:** Detects tampering.
  * **Used to secure:** HTTP (HTTPS), FTP (FTPS), SMTP (SMTPS), POP3 (POP3S), IMAP (IMAPS).
  * **TLS Handshake:**
    1.  ClientHello
    2.  ServerHello, Certificate, ServerKeyExchange, ServerHelloDone
    3.  ClientKeyExchange, ChangeCipherSpec
    4.  ChangeCipherSpec
  * **Relies on PKI:** Public Key Infrastructure, uses trusted certificate authorities to verify server identities.
### VI. Secure Shell (SSH)

  * **Purpose:** Secure remote access and file transfer.
  * **Port:** 22 (TCP).
  * **Features:**
      * Server authentication.
      * Encrypted communication.
      * Message integrity checks.
  * **Authentication Methods:**
      * Password.
      * Public key.
  * **Example:** `ssh <username>@<machine_ip>`
  * **Secure Copy (SCP):** `scp <file> <username>@<machine_ip>:<remote_path>`
### VII. Password Attacks

  * **Types:**
      * Password Guessing.
      * Dictionary Attack.
      * Brute-force Attack.
  * **Tools:**
      * Hydra: [https://github.com/vanhauser-thc/thc-hydra](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/vanhauser-thc/thc-hydra)
      * Wordlists (e.g., RockYou: `/usr/share/wordlists/rockyou.txt`)
  * **Hydra Usage:**
    ```
    hydra -l <username> -P <wordlist> <server> <service>
    ```
  * **Options:**
      * `-s <port>`: Non-default port.
      * `-V` or `-vV`: Verbose output.
      * `-t <number>`: Number of parallel connections.
      * `-d`: Debugging output.
  * **Mitigation:**
      * Strong password policies.
      * Account lockout.
      * Throttling.
      * CAPTCHA.
      * Public key authentication.
      * Two-factor authentication.
### VIII. Protocol Summary

| Protocol | TCP Port | Application(s) | Data Security |
|---|---|---|---|
| FTP | 21 | File Transfer | Cleartext |
| FTPS | 990 | File Transfer | Encrypted |
| HTTP | 80 | Worldwide Web | Cleartext |
| HTTPS | 443 | Worldwide Web | Encrypted |
| IMAP | 143 | Email (MDA) | Cleartext |
| IMAPS | 993 | Email (MDA) | Encrypted |
| POP3 | 110 | Email (MDA) | Cleartext |
| POP3S | 995 | Email (MDA) | Encrypted |
| SFTP | 22 | File Transfer | Encrypted |
| SSH | 22 | Remote Access and File Transfer | Encrypted |
| SMTP | 25 | Email (MTA) | Cleartext |
| SMTPS | 465 | Email (MTA) | Encrypted |
| Telnet | 23 | Remote Access | Cleartext |
