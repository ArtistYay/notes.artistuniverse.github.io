---
tags:
  - Microsoft Azure
  - Cybersecurity
---

## 1. Describe how you would design a secure, multi-account AWS and Azure environment for a SaaS company handling sensitive enterprise data.

1. Limit the blast radius and set up a hierarchy. AWS has Organizations, which lets you create [`Organizational Units (OUs)`](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous.html) based on the environment (like a Security OU), and under that OU you create separate accounts for each job (like a Log Archive account, Security Tooling account, Network account, etc.).

	Azure has Management Groups and Subscriptions. You can make management groups for Production, Non-Production, and so on, then isolate dev and test environments at the subscription level.

2. Identity and access management. Attackers don't have to work that hard exploiting vulnerabilities anymore when they can just scan the internet for leaked access keys and credentials. Having a single source of truth for identity helps a lot. I'm biased, so I'd say Entra ID should be your IdP and you federate AWS to it. In Entra ID you can use Privileged Identity Management (PIM) for just-in-time access to highly privileged roles that need approval. On the AWS side, IAM Identity Center hands out short-lived credentials through roles, so people don't need long-term IAM user access keys at all.

3. Network security and isolation. Segment your network with VNets (Azure) and VPCs (AWS), then use private endpoints. You don't want your database taking requests from the internet. Firewalls are also a great tool here, since they inspect traffic going in and out of your environment.

4. Data protection: at rest, in transit, and in use. Use customer-managed keys (CMKs) in AWS KMS and Azure Key Vault. That gives your company control over key rotation and revocation. And please never hard-code secrets... it wouldn't be a secret if you did. AWS Secrets Manager and Azure Key Vault exist so you can pull and rotate database credentials, API keys, and a lot more through code. You also need to know what data your company has and where it lives. May I suggest Microsoft Purview...

5. All of this sounds good, but without the right governance you won't get far, lol. You need a way to manage the complexity of multicloud, centralized visibility, and automated compliance. That means cloud security posture management (CSPM) like Defender for Cloud, AWS SCPs for hard guardrails (like stopping anyone from turning off logging, or only allowing resources in certain regions), and Azure Policy.
