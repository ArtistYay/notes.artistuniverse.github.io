### **I. Manual Discovery:**

- **Favicon:**
    - Website icon.
    ![screenshot](../../../images/Pasted image 20241101202710.png)
    - Default favicons can reveal frameworks used.
    - Use OWASP favicon database.
    - Get favicon hash with `curl https://example.com/favicon.ico | md5sum`.
- **HTTP Headers:**
    - Server information (web server software, scripting language).
    - Use `curl http://example.com -v`.
- **OSINT - Google Hacking/Dorking:**
    - Advanced Google search features.
    - **Filters:**
        - `site:` (e.g., `site:tryhackme.com`)
        - `inurl:` (e.g., `inurl:admin`)
        - `filetype:` (e.g., `filetype:pdf`)
        - `intitle:` (e.g., `intitle:admin`)
    - **Other Operators:**
        - `"exact phrase"`
        - `-` (exclude results)
    - **Advanced Search Operators List:** [https://github.com/cipher387/Advanced-search-operators-list](https://github.com/cipher387/Advanced-search-operators-list)
- **Wappalyzer:**
    - Browser extension and online tool.
    - Identifies website technologies (frameworks, CMS, payment processors, versions).
    - [https://www.wappalyzer.com/](https://www.wappalyzer.com/)
- **Wayback Machine:**
    - Historical archive of websites.
    - Uncover old pages that might still be active.
    - [https://archive.org/web/](https://archive.org/web/)
### **II. Automated Discovery:**

- **Purpose:** Quickly identify commonly named directories and files.
- **Wordlists:** SecLists ([https://github.com/danielmiessler/SecLists](https://github.com/danielmiessler/SecLists))
- **Tools:**
    - **ffuf:**
        ``` ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -u http://10.10.43.104/FUZZ```
    - **dirb (I like-ish):**
        ```dirb http://10.10.43.104/ /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt```
    - **gobuster(I like):**
        ```gobuster dir --url http://10.10.43.104/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt```