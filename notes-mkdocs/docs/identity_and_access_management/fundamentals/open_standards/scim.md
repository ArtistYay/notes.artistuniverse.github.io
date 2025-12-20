### SCIM

Let's pivot for a moment into user provisioning. Imma kept it a buck with you, this lifecycle management for different users is draining if you deal with it manually especially if you have hundreds or thousands of users. Imagine you have to even access to 20 people a day for a certain app or server.

This is where SCIM comes in, it automates the process of exchanging user identity (attributes) information or gives the admin the chance to automate the user lifecycle management.. For example, if a new employee is onboarding HR can create a new user in ServiceNow and put them in the sales group based on these attributes SCIM picks it up and sends it to salesforce. 

###### The process

1. You create the user "Tim" and tag him as "Department: Sales."
2. ServiceNow sends a SCIM message to Entra ID saying, "Create Tim, he is in Sales."
3. Entra ID creates the account. It has a rule: "If Department = Sales, add user to 'Salesforce_Users' group."
4. Entra ID sends a SCIM message to Salesforce saying, "Create Tim, and put him in the 'Salesforce_Users' group."
5. Salesforce receives the message. It sees "Tim" is in the "Salesforce_Users" group and automatically unlocks the Sales Dashboard.

This is where Entra ID Lifecycle Management comes in 😉

![screenshot](../../../images/scim.png)

[Blog Article | Okta](https://www.okta.com/blog/identity-security/what-is-scim/)

[Article | Microsoft](https://www.microsoft.com/en-us/security/business/security-101/what-is-scim)