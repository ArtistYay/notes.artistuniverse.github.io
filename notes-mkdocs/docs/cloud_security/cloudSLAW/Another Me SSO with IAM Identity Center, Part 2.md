---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- Permissions get handed out with something called a _permission set_. A permission set can have up to 10 AWS managed or customer managed policies (you can raise that to 20 with a quota increase) plus one inline policy.
- To give someone access to an account, you assign a user or group a permission set and the accounts. It's a 3 part equation: group + permission set + account = what you can do.
- Users and groups can have multiple permission sets per account.
- When you assign a permission set, Identity Center creates an IAM role in the account with the policies you picked. Then it sets the role's trust policy so the identity provider (IAM Identity Center) can assume it.

![screenshot](../../../images/another_me_p2.png)

## The Lab

1. Created an AdministratorAccess permission set.

    Relay state is just a fancy way of saying "when the user logs in with this permission set, drop them in this part of the console."

2. Gave the group AdministratorAccess to the SecurityAudit and management accounts.

    You have to select the accounts first, then click 'Assign users or groups'.

3. Looked at the `AWSReservedSSO_AdministratorAccess` role.

![screenshot](../../../images/Pasted image 20250309200237.png)

4. This is the ARN of the _identity provider_ that Identity Center/Organizations created in the account. You can see it under Identity providers. An AWS account can have more than one of these.
5. This gives the role permission to use the [AssumeRoleWithSAML](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithSAML.html) API call, which is a little different from AssumeRole but really similar.
6. This lets the IdP tag the session when you assume the role. That's really useful for tracking, because it adds a session name that matches the user who assumed the role.
7. The last part is a condition that ONLY allows this when you come through the sign-in portal, and ONLY the AWS one. You can't assume this role from anywhere else.
