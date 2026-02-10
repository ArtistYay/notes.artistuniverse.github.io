---
tags:
  - Azure
  - Questions
Date: 2023-08-10
---
1. In an Azure SQL Database, when writing audit logs to a storage account, what Azure Blob type are the logs written to?
    
    Append
    

1. You have an application running on Azure App Service and the data is hosted on an Azure SQL Database. The database stores confidential data about your employees and you followed the best practices to secure this data. You need to know about any attempts to steal data from your database immediately. How can you do so?
    
    Enable advanced data security and set up alerts for the database.
    

1. You need to enable SQL database auditing. On which two levels can an auditing policy be defined?
    
    Server-level and database-level
    

1. What is the difference between a standard and wildcard certificate?
    
    A standard certificate provides encryption for one domain, whereas a wildcard certificate provides encryption for multiple sub-domains.
    

1. Which column encryption method supports equality lookups, joins, and group by in Azure SQL Database?
    
    Collaborative
    

1. You have an application running on Azure App Service and the data is hosted on an Azure SQL Database. Currently the application connects through SQL authentication and the username and password are saved in application settings. Your security architect asked you not to store any usernames or passwords in application settings or anywhere else. What should you do to achieve that?
    
    Use managed identities to connect to the database.
    

1. At what layer does Azure Front Door Service operate?
    
    Layer 7
    

1. What is a feature you can use to battle malicious bot traffic?
    
    Rate limiting rules
    

1. Where there is an incoming request for an application that matches 4 NSG with priority 100, 500, 1000, and 5000. Which network security group (NSG) will be applied?
    
    The NSG with 100
    

1. A web application is running in Azure App Service and it accesses a storage account to read and write files. The storage account access keys are stored in an Azure Key Vault. You have a security regulation that directs you to rotate the storage account keys every week. How can you ensure the application will always read the latest keys from Key Vault?
    
    Create an Azure runbook that rotates the storage account keys and updates Key Vault with the latest keys.
    

1. You are binding a certificate to your application but Azure is failing because the domain has not been verified. What must you do to assure that Azure can verify the domain?
    
    Map a Canonical Name record (CNAME) to the App Service domain.
    

1. Which statement about the management plane and the data plane in Azure Key Vault is correct?
    
    The management plane is where you create and delete vaults, whereas the data plane allows you to work with the data stored in the key vault.