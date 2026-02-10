---
tags:
  - Microsot Azure
---

### Describe how you would design a secure, multi-account AWS and Azure environment for a SaaS company handling sensitive enterprise data.

1. Limit the blast radius and implement a hierarchy. In AWS, they have organizations which let you create [`Organizational Units (OUs)`](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous.html) which you can create based on the environment (eg, Security OU), and under that OU you can create a specific account for distinct functions (eg, Log Archive account, Security Tooling account, Network account, etc.)

	In Azure, there are Management Groups and Subscriptions. You can create Production, Non-Production, etc., and at the Subscription level, you can isolate by development/test environments.

2. Identity and access management, long are the days when attackers are exploiting vulnerabilities, but scanning the internet for leaked access keys and credentials. Having a single source of truth can help improve your security. I'm biased, so I would say Entra ID should be your IdP, and federate AWS to it. For Entra ID, you can implement Privileged Identity Management (PIM) to utilize Just-In-Time access to highly permissioned roles that require approval. AWS has the IAM Identity Center, which prohibits the use of access keys and instead provides temporary credentials via roles.

3. Network security and isolation. You want to segment your network with VNets (Azure) and VPCs (AWS), then implement private endpoints. You don't want your database to accept requests from the internet. Firewalls are also a magnificent security tool to implement, which inspects traffic entering and leaving your environment.

4. Data protection: at rest, in transit, and in use. Use Customer-Managed Keys (CMKs) in AWS KMS and Azure Key Vault. This gives your company control over key rotation and revocation. Please never hard-code secrets... it wouldn't be a secret if you did. AWS Secrets Manager and Azure Key Vault exist to programmatically retrieve and rotate database credentials, API keys, and much more. You also need to know what data your company has and where it is. May I suggest Microsoft Purview...

5. All of this sounds good, but without the proper governance, you will not get far, lol. Managing the complexity of a multi-cloud environment, centralized visibility, and automated compliance are required. Cloud Security Posture Management, AWS SCPs to set absolute guardrails (e.g., preventing the disablement of logging or restricting resource creation to specific regions), Azure Policy.