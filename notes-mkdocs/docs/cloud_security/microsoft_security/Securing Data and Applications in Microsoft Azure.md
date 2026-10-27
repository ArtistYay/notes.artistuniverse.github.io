---
tags:
  - Microsoft Azure
  - Cybersecurity
---

1. In an Azure SQL Database, when audit logs get written to a storage account, what blob type do they use?

    Append blobs

1. You have an app on Azure App Service with its data in an Azure SQL Database. The database stores confidential employee data and you followed the best practices to secure it. You need to know about any attempt to steal data from the database right away. What do you do?

    Turn on Microsoft Defender for SQL (this used to be called Advanced Data Security) and set up alerts for the database.

1. You need to turn on SQL database auditing. On which two levels can you define an auditing policy?

    Server level and database level

1. What's the difference between a standard and a wildcard certificate?

    A standard certificate covers one domain. A wildcard certificate covers all the subdomains under one domain (like `*.contoso.com`).

1. Which column encryption type supports equality lookups, joins, and group by in Azure SQL Database?

    Deterministic encryption (Always Encrypted). It always turns the same value into the same encrypted value, which is what makes the lookups work. The downside is someone might guess values by looking at patterns, especially if there are only a few possible values like True/False. Randomized encryption is more secure but you can't search or join on it. I originally had "Collaborative" here, which isn't a real option.

1. You have an app on Azure App Service with its data in an Azure SQL Database. Right now the app uses SQL authentication and the username and password are saved in application settings. Your security architect says no usernames or passwords stored anywhere. What do you do?

    Use a managed identity to connect to the database.

1. What layer does Azure Front Door operate at?

    Layer 7

1. What feature can you use to fight malicious bot traffic?

    Rate limiting rules

1. An incoming request matches 4 NSG rules with priorities 100, 500, 1000, and 5000. Which rule gets applied?

    The rule with priority 100. With NSG rules, the lower the number, the higher the priority, and processing stops at the first match.

1. A web app on Azure App Service reads and writes files in a storage account. The storage account access keys are stored in Azure Key Vault. A security regulation says you have to rotate the keys every week. How do you make sure the app always reads the latest keys from Key Vault?

    Create an Azure Automation runbook that rotates the storage account keys and updates Key Vault with the new ones. Even better today: skip keys completely and give the app a managed identity with an RBAC role on the storage account, so there's nothing to rotate.

1. You're binding a certificate to your app but Azure fails because the domain hasn't been verified. What do you have to do so Azure can verify the domain?

    Map a CNAME (Canonical Name) record to the App Service domain. Azure also uses an `asuid` TXT record to prove you own the domain.

1. Which statement about the management plane and the data plane in Azure Key Vault is correct?

    The management plane is where you create and delete vaults. The data plane is where you work with what's stored in the vault (keys, secrets, and certificates).
