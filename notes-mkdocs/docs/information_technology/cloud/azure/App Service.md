---
tags:
  - Azure
Keyword: Compute
---
- Azure App Service let’s you build, deploy, and scale enterprise-grade web, mobile, and API apps. Enables you to build and host web apps, background jobs, mobile back-ends, and RESTful APIs in the programming language of your choice without managing infrastructure. It offers automatic scaling and high availability.

- It’s a PaaS

- You can create a web app via portal, azure cli, powershell, and ARM

- Has integrated load balancing.

- Two types on plans:
    
    - Non isolated - app service is not inside a VNET.
        
        - Free and Shared (F1, D1) runs on shared VMs
        
        - Basic (B1, B2, B3)
        
        - Standard (S1, S2, S3) pricing is based on the number of instances you run, production workloads.
        
        - Premium v2 (P1v2, P2v2, P3v2)
        
        - Premium v3 (P1v3, P2v3, P3v3)
        
    
    - Isolated - dedicated environment that is exclusive to a single customer. Also called App Service Environment (ASE). Apps can connect over VPN to on-premises resources.