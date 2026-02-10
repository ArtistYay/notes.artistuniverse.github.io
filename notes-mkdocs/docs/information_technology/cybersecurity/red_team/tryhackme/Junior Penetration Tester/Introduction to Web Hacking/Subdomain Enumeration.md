### **I. What is a Subdomain?**

- Used to organize content on a website.
- _Example:_ `blog.yourdomainname.com`
### **II. Subdomain Discovery Methods:**

- **OSINT - SSL/TLS Certificates:**
    - Certificate Authorities (CAs) keep logs of certificates.
    - Searchable databases: crt.sh ([https://crt.sh](https://crt.sh/))
- **OSINT - Search Engines:**
    - Use `site:` operator with wildcards.
    - _Example:_ `site:*.domain.com -site:www.domain.com` (finds subdomains but excludes www).
- **DNS Bruteforce:**
    - Tools like `dnsrecon`.
- **OSINT - Sublist3r:**
    - Automates subdomain discovery.
- **Virtual Hosts:**
    - DNS records can be on private servers or in local `/etc/hosts` (Linux) or `c:\windows\system32\drivers\etc\hosts` (Windows) files.
    - Use `ffuf` if you have the IP address. This is a good way to test for virtual hosts.