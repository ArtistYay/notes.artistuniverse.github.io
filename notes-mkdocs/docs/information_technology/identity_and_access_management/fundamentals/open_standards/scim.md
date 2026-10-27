---
tags:
  - Cybersecurity
  - Identity & Access Management
---

Let's pivot for a moment into user provisioning. Imma keep it a buck with you, managing the lifecycle for all these users is draining if you do it manually, especially if you have hundreds or thousands of them. Imagine having to give 20 people a day access to a certain app or server.

This is where SCIM (System for Cross-domain Identity Management) comes in. It's a standard for automatically exchanging user identity info (attributes) between systems, so the admin can automate user lifecycle management. For example, when a new employee is onboarding, HR can create the user in ServiceNow and put them in the sales group, and based on those attributes SCIM picks it up and sends it all the way to Salesforce.

## The process

1. You create the user "Tim" and tag him as "Department: Sales."
2. ServiceNow sends a SCIM message to Entra ID saying, "Create Tim, he is in Sales."
3. Entra ID creates the account. It has a rule: "If Department = Sales, add user to 'Salesforce_Users' group."
4. Entra ID sends a SCIM message to Salesforce saying, "Create Tim, and put him in the 'Salesforce_Users' group."
5. Salesforce receives the message. It sees "Tim" is in the "Salesforce_Users" group and automatically unlocks the Sales Dashboard.

This is where Microsoft Entra ID Governance (lifecycle workflows) comes in 😉

[Blog Article | Okta](https://www.okta.com/blog/identity-security/what-is-scim/)

[Article | Microsoft](https://www.microsoft.com/en-us/security/business/security-101/what-is-scim)
