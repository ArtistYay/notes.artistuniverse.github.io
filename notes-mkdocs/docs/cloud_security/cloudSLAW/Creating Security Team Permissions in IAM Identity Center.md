---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- So nobody is running around with full admin all the time, give out different permission sets (read-only, full admin, IAM admin) in IAM Identity Center based on the task. That limits the damage from an accident or a compromised account.

## The Lab

1. Assigned the `AdministratorAccess` permission set to the Admin group for the `IAM`, `SecurityAudit`, `SecurityOperations`, and `TestAccount1` accounts.

    This is there for incident responders in case they need to "break glass" and jump into an account that's under active attack.

2. Created more groups: `SecurityAdministrators` and `IAM Administrators`.
3. Created more permission sets: `ReadOnly` and `IdentityCenterAdministrator`.

    `IdentityCenterAdministrator` uses the AWS managed policy `AWSSSOMemberAccountAdministrator`.
