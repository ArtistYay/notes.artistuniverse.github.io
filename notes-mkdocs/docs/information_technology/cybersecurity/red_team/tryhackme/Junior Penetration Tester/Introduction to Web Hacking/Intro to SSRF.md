### **I. What is SSRF?**

- Allows an attacker to make the web server send HTTP requests to arbitrary resources.
- Two Types:
    - **Returning Data:** Response data is visible to the attacker.
    - **Blind:** No direct response. Requires external HTTP logging (RequestBin, custom HTTP server, Burp Collaborator).
### **II. Finding SSRF:**

- Look for functionality that takes a URL as input (e.g., fetching external resources, webhooks, import/export features).
- Try modifying the URL to target internal resources (e.g., `127.0.0.1`, `localhost`, internal IP ranges).
- Observe the application's behavior for clues (error messages, response times).

![screenshot](../../../images/Pasted image 20241109160732.png)

### **III. Defeating SSRF Defenses:**

- **Deny List:** Blocks specific URLs or IP addresses.
    - **Bypass Methods:**
        - Alternative IP representations: `0.0.0.0`, `127.1`.
        - Subdomains pointing to blocked IPs.
        - Internal metadata IP: `169.254.169.254`.
        - Custom DNS records.
- **Allow List:** Only allows specific URLs or domains.
    - **Bypass Methods:**
        - Similar-looking URLs: `https://website.thm.attackers-domain.thm`.
- **Open Redirect:** The application redirects users to a URL provided in a parameter.
    - **Exploitation:** Use the open redirect to target internal resources. _Example:_ `https://website.thm/redirect?url=http://127.0.0.1/admin`.
### **IV. General SSRF Testing Strategy:**

1. **Identify potential endpoints:** Look for URL parameters or functionality that fetches external data.
2. **Test with internal IPs:** Try `127.0.0.1`, `localhost`, and internal IP ranges.
3. **Bypass filters:** Use the techniques described above.
4. **Observe responses:** Look for data from internal resources or error messages.
5. **Use external tools for blind SSRF:** RequestBin, custom HTTP server, Burp Collaborator.
6. **Document findings:** Record the vulnerable endpoint and the bypass method used.