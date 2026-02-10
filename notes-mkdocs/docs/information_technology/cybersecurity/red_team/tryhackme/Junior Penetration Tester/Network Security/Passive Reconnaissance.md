### I. Publicly Available Records

- **WHOIS:**
    
    - Protocol for querying domain registration information.
    - Uses TCP port 43.
    - Reveals registrar, contact info, creation/update/expiration dates, and nameservers.
    - RFC 3912: [https://www.ietf.org/rfc/rfc3912.txt](https://www.ietf.org/rfc/rfc3912.txt)
- **DNS Records:**
    
    - Contain information about a domain's IP addresses, mail servers, etc.
    - Queried using `nslookup` and `dig`.
### II. `nslookup` (Name Server Lookup)

- **Basic Usage:**
    
    - `nslookup <domain_name>` (e.g., `nslookup tryhackme.com`)
    - `nslookup <options> <domain_name> <server>`
- **Options:**
    
    - `A`: IPv4 address lookup (default)
    - `AAAA`: IPv6 address lookup
    - `MX`: Mail exchanger lookup
    - `NS`: Nameserver lookup
    - `CNAME`: Canonical name lookup
    - `PTR`: Reverse DNS lookup (IP to domain name)
- **Server:**
    
    - Optional. Specifies the DNS server to query.
    - Can be a public DNS server like Cloudflare (1.1.1.1, 1.0.0.1), Google (8.8.8.8, 8.8.4.4), or Quad9 (9.9.9.9, 149.112.112.112).
    - More public DNS servers: Search online for "public DNS"
### III. `dig` (Domain Information Groper)

- **More Advanced DNS Queries**
    
- **Basic Usage:**
    
    - `dig <domain_name>`
    - `dig <domain_name> <type>`
    - `dig @<server> <domain_name> <type>`
- **Type:** Same as `nslookup` options (A, AAAA, MX, NS, CNAME, PTR).
### IV. DNSDumpster

- **Web-based tool for DNS reconnaissance:** [https://dnsdumpster.com/](https://www.google.com/url?sa=E&source=gmail&q=https://dnsdumpster.com/)
- **Discovers subdomains:** Finds subdomains that might not be revealed by `nslookup` or `dig`.
- **Provides:**
    - List of DNS servers.
    - IP address resolution.
    - Geolocation of IP addresses.
    - Graphical representation of DNS data.
### V. Shodan

- **Search engine for internet-connected devices:** [https://www.shodan.io/](https://www.google.com/url?sa=E&source=gmail&q=https://www.shodan.io/)
- **"The search engine for everything else"**: Indexes devices like servers, webcams, routers, industrial control systems, etc.
- **Collects service information:** Banners, versions, open ports, etc.
- **Useful for:**
    - Finding specific devices.
    - Identifying vulnerable systems.
    - Researching internet-connected infrastructure.