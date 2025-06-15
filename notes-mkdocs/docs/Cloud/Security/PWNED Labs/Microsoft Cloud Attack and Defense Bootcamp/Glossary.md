*Write down every term you do not know. Attempt to define the terms in a way that makes sense to you. If you can’t find what a term means, that’s when you research or ask the dumb questions in an appropriate place. It will also serve as a reminder for how much you’ve learned when the day comes that everything seems easy to you*

1. `Invoke-WebRequest` is the equivalent of curl in PowerShell.
2. [`x-ms-version`](https://www.google.com/search?q=What+is+x-ms-version%3F&oq=What+is+x-ms-version%3F&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB7SAQg0Mjg2ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8) specifies the version against different azure resources.
3. Azure REST APIs specifically manage Azure resources like virtual machines and storage, while the Microsoft Graph API provides access to data across various Microsoft 365 services like Outlook, OneDrive, and Teams.
4. We can download and import the GraphRunner PowerShell script as before. It will be heavily signatured so we'll execute it from a whitelisted directory. 
	1. The phrase "heavily signatured" in this context means that the **GraphRunner PowerShell script** is likely well-known to security tools and antivirus solutions. Many cybersecurity vendors create **signatures**—unique identifiers based on the script's code or behavior—to detect and block potentially malicious scripts, especially post-exploitation tools like GraphRunner.
	2. **Heavily Signatured:**
    - The script's code or execution patterns are likely flagged by Endpoint Detection and Response (EDR) tools, antivirus software, or other security solutions.
    - This means if executed in a monitored environment, the script could trigger an alert or be outright blocked.
	3. . **Whitelisted Directory:**
    - A "whitelisted directory" is a folder or location in the file system that security tools or policies treat as **trusted** and less likely to be monitored or restricted.
    - Organizations often whitelist directories for legitimate software or internal tools to ensure business continuity without interference from security tools.
    - By placing the script in such a directory, attackers aim to bypass detection mechanisms.