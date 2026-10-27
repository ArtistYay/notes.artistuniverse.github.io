---
tags:
  - Microsoft Azure
  - Cybersecurity
---

!!! note "Name changes"
    These are practice questions from an older course. Azure Security Center is Microsoft Defender for Cloud now, and Azure Active Directory is Microsoft Entra ID. I left the old names in the questions but updated the answers.

1. What does the Azure Security Center investigation graph cover?

    A specific entity and the entities that are related to it.

1. In the Azure portal, you configure App Service authentication so all anonymous requests to `/.auth/login/<provider>` get redirected to the chosen provider. You get an anonymous request from a native mobile app. What response does the mobile app most likely get back?

    HTTP 401 Unauthorized. Browsers get redirected to the sign-in page (HTTP 302), but native mobile apps get a 401. I originally had HTTP 200 OK here, which is wrong.

1. Which feature encrypts data both at rest and in motion in an Azure SQL database?

    Always Encrypted. The data gets encrypted on the client side, so it stays encrypted in the database and on the way there, and even the DB admins can't read it.

1. When should you run a security playbook in Security Center?

    When you need to respond to a specific security alert. In Defender for Cloud this is called workflow automation, and it runs a Logic App.

1. Which operating systems are supported by the Microsoft Monitoring Agent?

    Windows and Linux VMs. The Microsoft Monitoring Agent (Log Analytics agent) was retired in August 2024 though, so use the Azure Monitor Agent (AMA) now. It also supports Windows and Linux.

1. In a Platform-as-a-Service (PaaS) model, which responsibility moves to Microsoft?

    Applying security patches to the operating system.

1. You want to connect a Windows VM to a Linux VM. Which protocol should you use and what kind of key?

    Secure Shell (SSH) and SSH keys.

1. What Azure service can you use for inbound protection at the perimeter?

    Azure Application Gateway (with its Web Application Firewall turned on).

1. What's the name of Azure's load balancer service that includes a web application firewall and protects HTTP traffic?

    Azure Application Gateway

1. You're reviewing Security Center recommendations and there's a vulnerability in a network security group. Which category is it?

    High severity

1. What protocol does Azure Active Directory use to authorize access to web apps and web APIs?

    OAuth 2.0
