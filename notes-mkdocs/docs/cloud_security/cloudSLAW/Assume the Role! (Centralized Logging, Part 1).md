---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lab

1. Assumed the `OrganizationAccountAccessRole`.

    You have to put in the account ID of the account you want to switch into (SecurityAudit) and the role name (OrganizationAccountAccessRole).

2. Deployed an S3 bucket in the SecurityAudit account for centralized logging.

    Centralizing logs is a big part of any cloud security strategy. With all the logs in one place, the security team can investigate and watch for suspicious activity across every account without hopping around.

## The Lesson

- _AWS doesn't let you assume roles with the root user. You have to use an IAM user or another role._
- AWS Security Token Service (STS) is the service that hands out temporary, limited-privilege credentials when you assume a role.

![screenshot](../../../images/Pasted image 20250309124139.png)
