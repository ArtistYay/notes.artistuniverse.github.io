---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lab

1. Turned on AWS Organizations.

    Organizations lets you manage a bunch of AWS accounts from one place, which is a best practice once you have more than one account. It gives you a clean way to split things up by business unit, environment, or security boundary.

2. Created an OU (Organizational Unit) named 'Security' and moved the 'LogArchive' account into it.

    OUs are containers for AWS accounts, so you can group accounts by business or security needs.

    OUs also let you apply Service Control Policies (SCPs), which control what's allowed in every account under that OU.

![screenshot](../../../images/Pasted image 20250309111741.png)

## The Lesson

- `OrganizationAccountAccessRole` lets the management account get into the new account as an administrator. It gets created automatically when you create an account from Organizations, and it means you don't have to manage separate IAM users in every account. In other words, the role trusts the whole management account, so anyone in the management account with permission to assume roles can use it.
- Service Control Policies (SCPs) restrict what actions are allowed in each account, which protects your sensitive resources.
- The account you turn Organizations on in becomes your management account. DO NOT DEPLOY WORKLOADS IN THAT ACCOUNT.
- With consolidated billing, member accounts roll their charges up to the management account but are otherwise still independent.
