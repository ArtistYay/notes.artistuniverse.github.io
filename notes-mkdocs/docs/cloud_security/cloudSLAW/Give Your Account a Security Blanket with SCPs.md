---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lab

1. Turned on Service Control Policies (SCPs).

    This attaches an allow-all SCP called `FullAWSAccess` to every OU and account. It basically says "nothing is blocked at the org level."

    Even with `FullAWSAccess` in place, users still need IAM permissions to actually use any services. The SCP doesn't give anyone access, it just doesn't take any away.

2. Made a custom SCP to protect the root user and stop accounts from leaving the organization.

    `ProtectRootAndOrg` denies the `organizations:LeaveOrganization` action and blocks the root user from doing anything.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "organizations:LeaveOrganization"
      ],
      "Resource": "*",
      "Effect": "Deny"
    },
    {
      "Action": "*",
      "Resource": "*",
      "Effect": "Deny",
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": [
            "arn:aws:iam::*:root"
          ]
        }
      }
    }
  ]
}
```

3. Applied the SCP at the 'Root' level.

    Now no account can remove itself from the organization or use its root user.

## The Lesson

- SCPs set the boundaries for what can happen in an account. They're like a filter on top of IAM policies at the organization level. SCPs never grant permissions by themselves. They set the maximum, and IAM policies still have to allow the action.
- In AWS, an explicit deny always wins over an allow, no matter where the allow comes from.
- SCPs don't apply to the management account, which is one more reason not to run anything in it.
- AWS also has centralized root access management now. From the management account (or a delegated admin), you can remove the root credentials from member accounts completely and do the few root-only tasks with short-term root sessions instead.
