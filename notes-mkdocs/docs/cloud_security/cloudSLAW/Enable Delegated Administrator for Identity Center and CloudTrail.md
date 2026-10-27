---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- Delegated administration lets you hand control of certain AWS services to other accounts. That keeps people out of the management account and spreads out admin responsibilities, which is least privilege at the account level.

    The management account has huge power over every account in the organization. A lot of AWS services need the management account to get set up, so people end up using it all the time. If it gets compromised, an attacker basically owns everything.

## The Lab

1. Delegated IAM Identity Center to the `IAM` account in the `Security` OU.

    Identity Center handles authentication and authorization for everyone, so it's a big deal. Delegating it means day-to-day admin work doesn't need the management account.

2. Delegated CloudTrail to the `SecurityAudit` account.
